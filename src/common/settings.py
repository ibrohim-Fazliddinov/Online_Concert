"""
common_settings.py

Модуль содержит базовый класс настроек `ConcertBaseSettings`,
который задаёт общие параметры для всех классов конфигурации приложения.

Переменные:
    env_file (str): Путь к файлу окружения, определяемый через `PathSettings.env_path`.

Классы:
    ConcertBaseSettings(BaseSettings):
        Базовый класс Pydantic-настроек с общей конфигурацией:
        - `env_file`: откуда читать переменные окружения.
        - `env_file_encoding`: кодировка файла (`utf-8`).
        - `case_sensitive`: нечувствительность к регистру имён переменных.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from settings.path import PathSettings

# Путь к файлу окружения, получаемый из PathSettings
env_file: str = PathSettings.env_path

class ConcertBaseSettings(BaseSettings):
    """
    Общий базовый класс для всех моделей настроек приложения.

    Конфигурация Pydantic:
        env_file (str): файл для загрузки переменных окружения.
        env_file_encoding (str): кодировка при чтении файла окружения.
        case_sensitive (bool): регистр имён переменных окружения не учитывается.
    """
    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
