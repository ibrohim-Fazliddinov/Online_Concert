"""
logging_settings.py

Модуль содержит класс `LoggingSetting` для настройки логирования через Pydantic `BaseSettings`.
Позволяет конфигурировать формат, файл, уровень и ротацию логов через переменные окружения.

Пример использования:

```python
import logging.config
from src.common.logging_settings import LoggingSetting

settings = LoggingSetting()
config = {
    "version": 1,
    "handlers": {
        "file": settings.to_handler_config()
    },
    "root": {
        "handlers": ["file"],
        "level": settings.LEVEL,
    }
}
logging.config.dictConfig(config)
```
"""

import json
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from src.common.enum import ConcertEnum


class LogFormat(ConcertEnum):
    """Доступные форматы вывода логов."""
    PRETTY = "pretty"
    JSON = "json"


class LogLevel(ConcertEnum):
    """Уровни логирования по стандарту logging."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingSetting(BaseSettings):
    """
    Конфигурация логирования.

    Атрибуты:
        LOG_FORMAT (LogFormat): формат вывода (pretty или json).
        LOG_FILE (Path): путь до файла логов.
        LEVEL (LogLevel): уровень логирования.
        MAX_BYTES (int): максимальный размер файла до ротации.
        BACKUP_COUNT (int): число архивных файлов при ротации.
        FILE_MODE (str): режим открытия файла ('a' - append).
        ENCODING (str): кодировка лог-файла.
        FILE_FORMAT (str): шаблон текстового формата логов.
        PRETTY_FORMAT (str): шаблон цветного форматирования для терминала.
        JSON_FORMAT (dict): структура полей для JSON-логов.

    Методы:
        formatter: возвращает строку форматтера в зависимости от LOG_FORMAT.
        to_handler_config: собирает конфигурацию обработчика для dictConfig.
    """

    LOG_FORMAT: LogFormat = LogFormat.PRETTY
    LOG_FILE: Path = Path("./logs/app.log") if os.name == "nt" else Path("/var/log/app.log")
    LEVEL: LogLevel = LogLevel.DEBUG
    MAX_BYTES: int = 10 * 1024 * 1024
    BACKUP_COUNT: int = 5
    FILE_MODE: str = "a"
    ENCODING: str = "utf-8"
    FILE_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    PRETTY_FORMAT: str = (
        "\033[1;36m%(asctime)s\033[0m - "
        "\033[1;32m%(name)s\033[0m - %(levelname)s - %(message)s"
    )
    JSON_FORMAT: dict = {
        "timestamp": "%(asctime)s",
        "level": "%(levelname)s",
        "module": "%(module)s",
        "function": "%(funcName)s",
        "message": "%(message)s",
    }

    class Config:
        """Настройки Pydantic для LoadingSetting."""
        env_prefix = "LOG_"
        use_enum_values = True

    @property
    def formatter(self) -> str:
        """
        Выбирает и возвращает нужный форматтер.

        :return: PRETTY_FORMAT, JSON_FORMAT (JSON-string) или FILE_FORMAT.
        """
        if self.LOG_FORMAT == LogFormat.PRETTY:
            return self.PRETTY_FORMAT
        elif self.LOG_FORMAT == LogFormat.JSON:
            # Структурированное логирование в формате JSON
            return json.dumps(self.JSON_FORMAT, ensure_ascii=False)
        return self.FILE_FORMAT

    def to_handler_config(self) -> dict:
        """
        Собирает конфигурацию обработчика логов для передачи в logging.config.dictConfig().

        :return: dict с настройками файло-ориентированного обработчика.
        """
        return {
            "level": self.LEVEL,
            "filename": str(self.LOG_FILE),
            "formatter": self.formatter,
            "maxBytes": self.MAX_BYTES,
            "backupCount": self.BACKUP_COUNT,
            "encoding": self.ENCODING,
            "mode": self.FILE_MODE,
            "force": True,
        }
