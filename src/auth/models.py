from sqlalchemy import String, LargeBinary, Enum
from sqlalchemy.orm import mapped_column, Mapped
from src.auth.enum import UserRoles
from src.common.model import Base


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
    """
    __tablename__ = "user_account"
    __table_args__ = {"schema": "user_core"}

    first_name: Mapped[str] = mapped_column(String(50))
    second_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True)
    role: Mapped[UserRoles] = mapped_column(Enum(UserRoles), default=UserRoles.client)
    password: Mapped[str] = mapped_column(LargeBinary)




    # posts: Mapped["Post"] = relationship(argument="Post", back_populates="user")
    # orders: Mapped["Orders"] = relationship(argument="Orders")
    # payment: Mapped["Payment"] = relationship(argument="Payment")



