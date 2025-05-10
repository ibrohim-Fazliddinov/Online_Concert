"""
Модуль: settings.py

Этот модуль настраивает глобальные параметры приложения
с использованием Pydantic BaseSettings.
"""
from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings
from settings.path import PathSettings

env_file_path, app_env = PathSettings.get_env_file_and_type()

class Settings(BaseSettings):
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

    dsn: str

    model_config = SettingsConfigDict(
        # **ConcertBaseSettings.model_config,
        env_file=env_file_path,
        env_prefix="POSTGRES_",
        extra="ignore"
    )

settings = Settings()