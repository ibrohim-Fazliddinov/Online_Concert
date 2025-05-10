from datetime import datetime, timedelta
from typing import Optional

import jwt

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.auth.constants import AUTH_ACCESS_TOKEN_EXPIRE_MINUTE, AUTH_TOKEN_ALGORITHM
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.auth.utils import hash_password, verify_password


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_phone(self, phone: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.phone_number == phone)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        # model_dump возвращает dict с полями схемы без служебных
        payload = user_data.model_dump(exclude={"password"})
        # создаём ORM-экземпляр
        user = User(**payload)
        # хэшируем пароль
        user.password = hash_password(user_data.password)

        self.session.add(user)
        await self.session.commit()
        # чтобы получить автоматически сгенерённые id, timestamps и т.п.
        await self.session.refresh(user)
        return user

    async def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.timestamp(datetime.now()) + AUTH_ACCESS_TOKEN_EXPIRE_MINUTE * 86400
        to_encode.update({"exp": expire, "sub": data.get("sub")})
        return jwt.encode(to_encode, 'goo', algorithm=AUTH_TOKEN_ALGORITHM)