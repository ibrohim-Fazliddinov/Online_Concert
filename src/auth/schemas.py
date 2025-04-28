# PYDANTIC MODELS
from typing import Optional, Any
from pydantic import BaseModel, EmailStr, field_validator
from src.auth.utils import hash_password, generate_password
from src.common.schema_base import ConcertBase


class UserBase(ConcertBase):
    """Базовая схема пользователя с личными данными."""

    first_name: str
    second_name: str
    email: EmailStr
    phone_number: str

    # TODO: добавить валидацию email и phone_number


class UserLogin(BaseModel):
    """Схема для запроса авторизации пользователя."""

    email: EmailStr
    password: str


class UserRegister(UserLogin):
    """Схема для запроса регистрации пользователя."""

    password: Optional[str] = None

    @field_validator("password")
    def password_required(cls, value: Any) -> str:
        """Хэшировать переданный пароль или сгенерировать и захэшировать новый, если пароль не указан."""
        password = value or generate_password()
        return hash_password(password)


class UserLoginResponse(ConcertBase):
    """Схема для ответа при авторизации пользователя (с токеном)."""

    token: Optional[str] = None


class UserRead(UserBase):
    """Схема для чтения информации о пользователе."""

    id: int


class UserPasswordUpdate(BaseModel):
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


class UserCreate(BaseModel):
    """Схема для создания нового пользователя."""

    first_name: str
    second_name: str
    email: EmailStr
    phone_number: str
    password: Optional[str] = None
    role: Optional[str] = None

    @field_validator("password")
    def hash(cls, value: Optional[str]) -> Optional[str]:
        """Хэшировать пароль пользователя, если он указан."""
        if value is not None:
            return hash_password(str(value))
        return value


class UserRegisterResponse(BaseModel):
    """Схема для ответа при регистрации пользователя (с токеном)."""

    token: Optional[str] = None
