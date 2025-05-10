"""
auth/config.py

Модуль содержит Pydantic-модели для настройки и валидации конфигурации аутентификации.
Переменные загружаются из файла окружения, путь к которому определяется через PathSettings.
Все поля корректно типизируются и проходят валидацию благодаря Pydantic и BaseSettings.

Пример использования:

    from auth.config import AuthSettings

    settings = AuthSettings()
    print(settings.AUTH_URL)
    google_conf = settings.AUTH_OAUTH_GOOGLE
    print(google_conf.client_id)

"""
import inspect

from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict
from src.common.settings import ConcertBaseSettings
from src.auth import constants as const

# print(inspect.signature(SettingsConfigDict))

class BaseAuthConfigSetting(ConcertBaseSettings):
    """
    Базовый класс настроек аутентификации.

    Наследует `ConcertBaseSettings` и устанавливает префикс для переменных окружения:
        - env_prefix: "AUTH_"
    Это позволяет загружать все переменные окружения, начинающиеся с AUTH_.
    """
    model_config = SettingsConfigDict(
        **ConcertBaseSettings.model_config,
    )


class OAuthProviderSettings(ConcertBaseSettings):
    """
    Конфигурация одного OAuth-провайдера.

    Атрибуты:
        client_id (str): Идентификатор приложения у провайдера.
        client_secret (SecretStr): Секретный ключ клиента (будет скрыт в логах).
        auth_url (str): URL для перенаправления пользователя за кодом авторизации.
        token_url (str): URL для обмена кода на токен доступа.
        user_info_url (str): URL для получения информации о пользователе по access_token.
        scope (str): Запрашиваемые права доступа (space-separated).
        callback_url (str): URL-обработчик редиректа после авторизации.

    Все поля загружаются из переменных окружения с префиксом AUTH_OAUTH_GOOGLE__* при использовании в AuthSettings.
    """
    client_id: str
    client_secret: SecretStr
    auth_url: str
    token_url: str
    user_info_url: str
    scope: str
    callback_url: str


class AuthSettings(BaseAuthConfigSetting):
    """
    Основные настройки модуля аутентификации.

    Переменные окружения:
        Префикс: AUTH_
        Файл: задаётся через PathSettings.env_path
        Регистрозависимость: отключена (case_sensitive=False)

    Атрибуты:
        AUTH_URL (str): Базовый путь к auth-эндпоинтам (например, '/api/auth').

        # JWT-настройки
        AUTH_TOKEN_TYPE (str): Тип токена в заголовке Authorization (Bearer).
        AUTH_TOKEN_EXPIRE_MINUTES (int): Время жизни access-токена в минутах.
        AUTH_VERIFICATION_TOKEN_EXPIRE_MINUTES (int): Время жизни верификационного токена.
        AUTH_TOKEN_ALGORITHM (str): Алгоритм подписи JWT (например, HS256).
        AUTH_TOKEN_SECRET_KEY (SecretStr): Секретный ключ для подписи JWT.
        AUTH_USER_INACTIVE_TIMEOUT (int): Время неактивности пользователя (секунды).

        # SMTP-настройки
        AUTH_SMTP_SERVER (str): Адрес SMTP-сервера.
        AUTH_SMTP_PORT (int): Порт SMTP-сервера.
        AUTH_SENDER_EMAIL (str): Email отправителя.
        AUTH_SMTP_USERNAME (str): Логин для SMTP.
        AUTH_SMTP_PASSWORD (SecretStr): Пароль для SMTP.
    """
    AUTH_URL: str = "/api/auth"

    AUTH_TOKEN_TYPE: str = const.AUTH_TOKEN_TYPE
    AUTH_TOKEN_EXPIRE_MINUTES: int = const.AUTH_ACCESS_TOKEN_EXPIRE_MINUTE
    AUTH_VERIFICATION_TOKEN_EXPIRE_MINUTES: int = const.AUTH_VERIFICATION_TOKEN_EXPIRE_MINUTES
    AUTH_TOKEN_ALGORITHM: str = const.AUTH_TOKEN_ALGORITHM
    AUTH_TOKEN_SECRET_KEY: SecretStr
    AUTH_USER_INACTIVE_TIMEOUT: int = const.AUTH_USER_INACTIVE_TIMEOUT


    AUTH_SMTP_SERVER: str = "gmail.smtp"
    AUTH_SMTP_PORT: int = 587
    AUTH_SENDER_EMAIL: str = "noreply@gmail.com"
    AUTH_SMTP_USERNAME: str = "your_username"
    AUTH_SMTP_PASSWORD: SecretStr


class OAut2Settings(BaseAuthConfigSetting):
    """
    Дополнительные OAuth-настройки.

    Атрибуты:
        AUTH_OAUTH_SUCCESS_REDIRECT_URI (str): URI для успешного редиректа после OAuth.
        AUTH_OAUTH_CALLBACK_BASE_URL (str): Базовый URL для колбэков OAuth.
        AUTH_OAUTH_GOOGLE (OAuthProviderSettings): Конфигурация Google OAuth-провайдера.
    """
    AUTH_OAUTH_SUCCESS_REDIRECT_URI: str
    AUTH_OAUTH_CALLBACK_BASE_URL: str
    AUTH_OAUTH_GOOGLE: OAuthProviderSettings

