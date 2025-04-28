import os
from datetime import datetime, timedelta
import bcrypt
import jwt
from sqlalchemy import String, LargeBinary, Enum
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from src.auth.enum import UserRoles
from src.auth.utils import hash_password


class Base(DeclarativeBase):
    pass



class User(Base):
    """
    Модель пользователя в системе.

    Этот класс представляет пользователя и его данные в базе данных. Он содержит информацию
    о пользователе, такую как имя, фамилия, email, телефон и пароль. Также в классе реализованы
    методы для установки и проверки пароля, а также для генерации JWT токенов.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        first_name (str): Имя пользователя.
        second_name (str): Фамилия пользователя.
        email (str): Электронная почта пользователя, уникальная.
        phone_number (str): Номер телефона пользователя, уникальный.
        password (bytes): Захешированный пароль пользователя.

    Методы:
        verify_password(password: str) -> bool:
            Проверяет, совпадает ли переданный пароль с сохраненным хешированным паролем.

        set_password(password: str) -> None:
            Устанавливает новый пароль для пользователя, хешируя его перед сохранением.

        token (property) -> str:
            Генерирует JWT токен для пользователя, который можно использовать для аутентификации.
    """
    __tablename__ = "user_account"
    __table_args__ = {"schema": "user_core"}

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    second_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True)
    role: Mapped[UserRoles] = mapped_column(Enum(UserRoles), default=UserRoles.client)
    password: Mapped[str] = mapped_column(LargeBinary, nullable=False)

    def verify_password(self, password: str) -> bool:
        """
        Проверяет, совпадает ли переданный пароль с сохраненным хешированным паролем.

        Аргументы:
            password (str): Пароль для проверки.

        Возвращает:
            bool: Возвращает True, если пароли совпадают, иначе False.
        """
        if not password or not self.password:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def set_password(self, password: str) -> None:
        """
        Устанавливает новый пароль для пользователя, хешируя его перед сохранением.

        Аргументы:
            password (str): Пароль для установки.

        Исключения:
            ValueError: Если пароль пустой.
        """
        if not password:
            raise ValueError("Password cannot be empty")
        self.password = hash_password(password)

    @property
    def token(self):
        """
        Генерирует JWT токен для пользователя, который можно использовать для аутентификации.

        Токен содержит email пользователя и время его истечения.

        Возвращает:
            str: Закодированный JWT токен.
        """
        now = datetime.now()
        exp = (now + timedelta(seconds=86400)).timestamp()  # Время истечения токена - 24 часа
        data = {
            "exp": exp,
            "email": self.email,
        }
        secret_key = os.getenv("JWT_SECRET", "default_secret")  # Получаем секретный ключ из переменной окружения
        return jwt.encode(data, secret_key, algorithm="HS256")






    # posts: Mapped["Post"] = relationship(argument="Post", back_populates="user")
    # orders: Mapped["Orders"] = relationship(argument="Orders")
    # payment: Mapped["Payment"] = relationship(argument="Payment")



