"""
Модуль: settings.py

Этот модуль настраивает глобальные параметры приложения
с использованием Pydantic BaseSettings.
"""
from pydantic_settings import SettingsConfigDict
from src.common.settings import ConcertBaseSettings
from src.database import DatabaseSettings

class Settings(ConcertBaseSettings):
    """
    Pydantic-класс настроек основного приложения.

    Атрибуты:
        TITLE (str): Заголовок приложения.
        DESCRIPTION (str): Описание приложения.
        VERSION (str): Текущая версия приложения.
        HOST (str): Хост для запуска сервера.
        PORT (str): Порт для запуска сервера.
    """
    TITLE: str = "Online_Concert"
    DESCRIPTION: str = "CONCERT.RU CLONE"
    VERSION: str = '0.0.1'
    HOST: str = "0.0.0.0"
    PORT: str = "8000"

    @property
    def db(self) -> DatabaseSettings:
        """
        Создает экземпляр DatabaseSettings
        на основе переменных окружения.

        Возвращает:
            DatabaseSettings: Конфигурация для подключения к БД.
        """
        return DatabaseSettings(
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            db=self.POSTGRES_DB,
            echo=True,
            pool_size=10,
        )

    model_config = SettingsConfigDict(
        **ConcertBaseSettings.model_config,
        extra="allow"
    )