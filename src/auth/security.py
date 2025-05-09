from uuid import uuid4, UUID
import jwt
from jose import JWTError
from starlette import status
from src.auth import constants as const
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Any
from src.auth.models import User
from src.auth.schemas import UserRead
from src.auth.service import UserService
from src.common.redis import redis_client
import logging
from src.database import get_db_session

logger = logging.getLogger(__name__)



oauth2_scheme = OAuth2PasswordBearer(auto_error=False, scheme_name="Bearer", tokenUrl='api/auth/')


class AuthSecurity:
    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
        user_svc: UserService = Depends(),
        token: Optional[str] = Depends(oauth2_scheme),
    ):
        self.session = session
        self.user_svc = user_svc
        self.token = token

    async def register(self, name: str, email: str, password: str) -> dict:
        user = await self.user_svc.register_user(name, email, password)
        tokens = await self._create_tokens(user.id)
        return {"user": user, **tokens}

    async def login(self, email: str, password: str) -> dict:
        user = await self.user_svc.authenticate_user(email, password)
        tokens = await self._create_tokens(user.id)
        await self._store_refresh_token(user.id, tokens["refresh_token"])

        # 3) возвращаем вместе с Pydantic-схемой
        user_data = UserRead.model_validate(user)
        return {"user": user_data, **tokens}

    async def refresh(self, user_id: UUID, refresh_token: str) -> dict:
        if not await self._is_refresh_token_valid(user_id, refresh_token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        return await self._create_tokens(user_id)

    async def revoke(self, user_id: UUID) -> Any:
        await redis_client.delete(f"user:{user_id}:refresh")

    async def get_current_user(self) -> User:
        if not self.token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            payload = jwt.decode(
                self.token,
                const.AUTH_TOKEN_SECRET_KEY,
                algorithms=[const.AUTH_TOKEN_ALGORITHM],
                options={"require": ["exp","iat","nbf","sub","type"]},
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if payload["type"] != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            user_id = int(payload["sub"])
        except (KeyError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token subject",
                headers={"WWW-Authenticate": "Bearer"},
            )

        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    # — внутренние методы —
    async def _create_tokens(self, user_id: UUID) -> dict:
        now = datetime.now(timezone.utc)
        jti_a, jti_r = str(uuid4()), str(uuid4())

        access_payload = {
            "sub": str(user_id), "type": "access", "jti": jti_a,
            "iat": now, "nbf": now,
            "exp": now + timedelta(minutes=const.AUTH_ACCESS_TOKEN_EXPIRE_MINUTE),
        }
        refresh_payload = {
            "sub": str(user_id), "type": "refresh", "jti": jti_r,
            "iat": now, "nbf": now,
            "exp": now + timedelta(days=const.AUTH_REFRESH_TOKEN_EXPIRE_DAY),
        }

        access_token = jwt.encode(access_payload, const.AUTH_TOKEN_SECRET_KEY, algorithm=const.AUTH_TOKEN_ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, const.AUTH_TOKEN_SECRET_KEY, algorithm=const.AUTH_TOKEN_ALGORITHM)

        await redis_client.set(
            f"user:{user_id}:refresh",
            jti_r,
            ex=const.AUTH_REFRESH_TOKEN_EXPIRE_DAY * 86400,
        )

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}

    async def _is_refresh_token_valid(self, user_id: UUID, refresh_token: str) -> bool:
        try:
            payload = jwt.decode(
                refresh_token,
                const.AUTH_TOKEN_SECRET_KEY,
                algorithms=[const.AUTH_TOKEN_ALGORITHM],
            )
        except JWTError:
            return False

        if payload.get("type") != "refresh":
            return False

        stored = await redis_client.get(f"user:{user_id}:refresh")
        return stored == payload.get("jti")

    async def _store_refresh_token(self, user_id: UUID, refresh_token: str):
        await redis_client.set(
            f"user:{user_id}:refresh_token",
            refresh_token,
            ex=const.AUTH_REFRESH_TOKEN_EXPIRE_DAY * 86400,
        )
