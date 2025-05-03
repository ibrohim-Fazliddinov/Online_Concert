"""
Модуль: database.py

Этот модуль настраивает асинхронное подключение к PostgreSQL
с помощью SQLAlchemy и Pydantic.
"""

from typing import Dict, Any, AsyncGenerator
from pydantic import SecretStr, PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from settings.config import Settings
from src.common.settings import ConcertBaseSettings

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@0.0.0.0:5434/postgres_db"
"""
Резервная строка подключения. Рекомендуется использовать `settings.db.database_url` вместо неё.
"""


class DatabaseSettings(ConcertBaseSettings):
    """
    Pydantic-класс настроек для асинхронного подключения к PostgreSQL.

    Атрибуты:
        POSTGRES_USER (str): Имя пользователя базы данных.
        POSTGRES_PASSWORD (SecretStr): Пароль доступа к базе данных.
        POSTGRES_HOST (str): Адрес хоста (по умолчанию: localhost).
        POSTGRES_PORT (int): Порт соединения (по умолчанию: 5432).
        POSTGRES_DB (str): Название базы данных.
    """
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    @property
    def database_dsn(self) -> PostgresDsn:
        """
        Формирует DSN для подключения через asyncpg.

        Возвращает:
            PostgresDsn: Полный DSN, включающий схему, пользователя, пароль, хост, порт и базу данных.
        """
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=f"/{self.POSTGRES_DB}",
        )

    @property
    def database_url(self) -> str:
        """
        Получение строки подключения к базе данных для синхронных инструментов (например, Alembic).

        Возвращает:
            str: URL подключения к базе данных.
        """
        return str(self.database_dsn)

    @property
    def engine_params(self) -> Dict[str, Any]:
        """
        Параметры при создании SQLAlchemy Engine.

        Возвращает:
            Dict[str, Any]: Аргументы для create_async_engine (например, echo).
        """
        return {"echo": True}

    @property
    def session_params(self) -> Dict[str, Any]:
        """
        Параметры при создании асинхронной сессии SQLAlchemy.

        Возвращает:
            Dict[str, Any]: Аргументы для async_sessionmaker
                (autocommit, autoflush, expire_on_commit, класс сессии).
        """
        return {
            "autocommit": False,
            "autoflush": False,
            "expire_on_commit": False,
            "class_": AsyncSession,
        }


# Создание глобального экземпляра настроек
settings = Settings()
"""
Глобальный экземпляр настроек приложения.
"""

# Инициализация асинхронного движка SQLAlchemy
engine = create_async_engine(
    settings.db.database_url,
    **settings.db.engine_params,
)
"""
Асинхронный движок SQLAlchemy для работы с БД.
"""

# Фабрика асинхронных сессий
SessionLocal = async_sessionmaker(
    bind=engine,
    **settings.db.session_params
)
"""
Фабрика для создания экземпляров AsyncSession.
"""


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для FastAPI, возвращающая сессию БД.

    Возвращает:
        AsyncSession: Сессия базы данных для текущего запроса.
    """
    async with SessionLocal() as session:
        yield session
