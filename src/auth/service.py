from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.auth.models import User
from src.auth.schemas import UserRead
from src.auth.utils import hash_password, verify_password


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create_user(self, name: str, email: str, hashed_password: str) -> User:
        user = User(first_name=name, email=email, password=hashed_password)
        async with self.session.begin():
            self.session.add(user)
        await self.session.refresh(user)
        return user

    async def register_user(self, name: str, email: str, password: str) -> UserRead:
        if await self.get_user_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        hashed = hash_password(password)
        try:
            orm_user = await self.create_user(name, email, hashed)
        except IntegrityError:
            # если уникальность всё же нарушилась на уровне БД
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        # Pydantic v2: конвертация из ORM-модели
        return UserRead.model_validate(orm_user)

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        return user


