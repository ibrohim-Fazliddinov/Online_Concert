"""
Settings.py

Модуль содержит класс `Settings` для конфигурации приложения через Pydantic `BaseSettings`.
Все параметры могут быть заданы через переменные окружения, файл `.env`, либо брать значения по умолчанию.
"""
from typing import Dict, Any
import logging
from pydantic import SecretStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession
from settings.path import PathSettings

log = logging.getLogger(__name__)
env = PathSettings.env_path


class Settings(BaseSettings):
    """
    Основные настройки приложения.

    Атрибуты:
        TITLE (str): Название приложения.
        DESCRIPTION (str): Описание приложения.
        VERSION (str): Версия приложения.
        HOST (str): Хост для сервера.
        PORT (str): Порт для сервера.

        POSTGRES_USER (str): Пользователь БД PostgreSQL.
        POSTGRES_PASSWORD (SecretStr): Пароль пользователя БД (секрет).
        POSTGRES_HOST (str): Хост базы данных (по умолчанию 'localhost').
        POSTGRES_PORT (int): Порт базы (по умолчанию 5432).
        POSTGRES_DB (str): Имя базы данных.

        AUTH_URL (str): URL маршрута для аутентификации.
        TOKEN_*: Параметры JWT-токенов (тип, алгоритм, время жизни).

        SMTP_SERVER (str), SMTP_PORT (int), SENDER_EMAIL (str), SMTP_USERNAME (str), SMTP_PASSWORD (SecretStr):
            Параметры SMTP для отправки почты.

        OAUTH_PROVIDERS (Dict[str, Dict[str, str | int]]):
            Конфигурация OAuth-провайдеров (Google и т.д.).

    Свойства:
        database_dsn -> PostgresDsn:
            DSN для подключения к PostgreSQL через asyncpg.
        database_url -> str:
            Строка подключения для Alembic и других инструментов.
        engine_params -> Dict[str, Any]:
            Параметры для создания SQLAlchemy Engine.
        session_params -> Dict[str, Any]:
            Параметры для создания AsyncSession.

    Конфигурация BaseSettings:
        env_file (str): путь к файлу окружения, берётся из `PathSettings.env_path`.
        env_file_encoding (str): 'utf-8'.
        extra (str): 'allow' — разрешать дополнительные поля.
        case_sensitive (bool): False — имена переменных нечувствительны к регистру.
    """
    TITLE: str = "Online_Concert"
    DESCRIPTION: str = "CONCERT.RU CLONE"
    VERSION: str = '0.0.1'
    HOST: str = "0.0.0.0"
    PORT: str = "8000"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    @property
    def database_dsn(self) -> PostgresDsn:
        """
        Конструирует DSN для подключения к PostgreSQL через asyncpg.

        :return: Экземпляр PostgresDsn с заполненными параметрами.
        """
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @property
    def database_url(self) -> str:
        """
        Возвращает строку подключения к базе данных для Alembic и других инструментов.
        """
        return str(self.database_dsn)

    @property
    def engine_params(self) -> Dict[str, Any]:
        """
        Параметры для создания SQLAlchemy Engine.

        :return: Словарь дополнительных опций Engine.
        """
        return {"echo": True}

    @property
    def session_params(self) -> Dict[str, Any]:
        """
        Параметры для создания асинхронной сессии SQLAlchemy.

        :return: Словарь с автокоммитом, autoflush, expiration и классом сессии.
        """
        return {
            "autocommit": False,
            "autoflush": False,
            "expire_on_commit": False,
            "class_": AsyncSession,
        }

    # Настройки аутентификации
    AUTH_URL: str = "api/auth"
    TOKEN_TYPE: str = "Bearer"
    TOKEN_EXPIRE_MINUTES: int = 1440
    VERIFICATION_TOKEN_EXPIRE_MINUTES: int = 1440
    TOKEN_ALGORITHM: str = "HS256"
    TOKEN_SECRET_KEY: SecretStr
    USER_INACTIVE_TIMEOUT: int = 900

    # Настройки почты
    SMTP_SERVER: str = "mail.ru"
    SMTP_PORT: int = 587
    SENDER_EMAIL: str = "noreply@equiply.ru"
    SMTP_USERNAME: str = "admin"
    SMTP_PASSWORD: SecretStr

    # OAuth провайдеры
    OAUTH_SUCCESS_REDIRECT_URI: str = "https://online_concert.com"
    OAUTH_CALLBACK_BASE_URL: str = "api/oauth/{provider}/callback"
    OAUTH_PROVIDERS: Dict[str, Dict[str, str | int]] = {
        "google": {
            "client_id": "",
            "client_secret": "",
            "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_url": "https://oauth2.googleapis.com/token",
            "user_info_url": "https://www.googleapis.com/oauth2/v2/userinfo",
            "scope": "email profile",
            "callback_url": "http://localhost:8000/api/v1/oauth/google/callback",
        },
    }

    model_config = SettingsConfigDict(
        env_file=env,
        env_file_encoding="utf-8",
        extra="allow",
        case_sensitive=False,
    )
