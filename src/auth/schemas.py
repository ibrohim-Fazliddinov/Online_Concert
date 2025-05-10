# PYDANTIC MODELS
from typing import  Any, Literal
from uuid import UUID

from pydantic import EmailStr, field_validator
from pydantic.v1 import UUID1

from src.auth.enum import UserRoles
from src.auth.utils import hash_password, generate_password
from src.common.schema import ConcertBaseSchema, BaseConcertResponseSchema, BaseConcertRequestSchema


class UserBase(ConcertBaseSchema):
    """Базовая схема пользователя с личными данными."""

    first_name: str
    second_name: str
    email: EmailStr
    phone_number: str

class UserCreate(BaseConcertRequestSchema):
    """Схема для создания нового пользователя."""

    first_name: str
    second_name: str
    email: EmailStr
    phone_number: str
    password: str
    role: UserRoles | None


class UserRead(UserBase):
    """Схема для чтения информации о пользователе."""

    id: UUID


class UserUpdate(BaseConcertRequestSchema):
    first_name:  str | None
    last_name: str | None
    phone_number: str | None
    email: EmailStr | None


class UserLogin(BaseConcertRequestSchema):
    """Схема для запроса авторизации пользователя."""

    email: EmailStr
    password: str


class UserLoginResponse(BaseConcertResponseSchema):
    """Схема для ответа при авторизации пользователя (с токеном)."""

    access_token: str | None


class UserRegister(UserBase, BaseConcertRequestSchema):
    """Схема для запроса регистрации пользователя."""

    password: str | None

    @field_validator("password")
    def password_required(cls, value: Any) -> str:
        """Хэшировать переданный пароль или сгенерировать и захэшировать новый, если пароль не указан."""
        password = value or generate_password()
        return hash_password(password)


class UserRegisterResponse(BaseConcertResponseSchema):
    """Схема для ответа при регистрации пользователя (с токеном)."""

    access_token: str | None
    refresh_token: str | None


class PasswordResetRequest(BaseConcertRequestSchema):
    email: EmailStr


class PasswordResetConfirm(BaseConcertRequestSchema):
    token: str
    new_password: str


class UserPasswordUpdate(BaseConcertRequestSchema):
    """Схема для запроса на обновление пароля пользователя."""

    current_password: str
    new_password: str

    @field_validator("new_password")
    def validate_password(cls, value: str) -> str:
        """Проверка нового пароля на соответствие требованиям безопасности."""
        if not value or len(value) < 8:
            raise ValueError("Пароль должен быть не короче 8 символов")
        if not any(c.isdigit() for c in value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not (any(c.isupper() for c in value) and any(c.islower() for c in value)):
            raise ValueError("Пароль должен содержать как заглавные, так и строчные буквы")
        return value


class TokenResponseData(BaseConcertResponseSchema):
    access_token:  str
    # refresh_token: str
    token_type:    Literal["bearer"] = "bearer"
    # expires_in:    int


class TokenRefreshRequest(BaseConcertRequestSchema):
    refresh_token: str

#
# class TokenRefreshResponse(TokenData):
#     ...