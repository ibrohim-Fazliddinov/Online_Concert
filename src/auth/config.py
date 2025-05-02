"""
auth/config.py

Модуль содержит Pydantic-модели для конфигурации модуля аутентификации.
Переменные загружаются из файла окружения, путь к которому определяется через PathSettings.
Все поля корректно типизируются и проходят валидацию.

Пример использования:

    from auth.config import AuthSettings

    settings = AuthSettings()
    print(settings.AUTH_URL)
    google_conf = settings.AUTH_OAUTH_GOOGLE
    print(google_conf.client_id)

"""

from pydantic import SecretStr, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from settings.path import PathSettings


class OAuthProviderSettings(BaseSettings):
    """
    Конфигурация одного OAuth-провайдера.

    Атрибуты:
        client_id (str): Идентификатор приложения у провайдера.
        client_secret (SecretStr): Секретный ключ клиента (будет скрыт в логах).
        auth_url (AnyUrl): URL для перенаправления пользователя за кодом авторизации.
        token_url (AnyUrl): URL для обмена кода на токен доступа.
        user_info_url (AnyUrl): URL для получения информации о пользователе по access_token.
        scope (str): Запрашиваемые права доступа (space-separated).
        callback_url (AnyUrl): URL-обработчик редиректа после авторизации.

    Все поля загружаются из переменных окружения с префиксом AUTH_OAUTH_GOOGLE__* при использовании в AuthSettings.
    """
    client_id: str
    client_secret: SecretStr
    auth_url: AnyUrl
    token_url: AnyUrl
    user_info_url: AnyUrl
    scope: str
    callback_url: AnyUrl


class AuthSettings(BaseSettings):
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

        # OAuth-настройки
        AUTH_OAUTH_SUCCESS_REDIRECT_URI (AnyUrl): URL редиректа при успешном OAuth.
        AUTH_OAUTH_CALLBACK_BASE_URL (AnyUrl): Базовый шаблон callback-URL '/api/oauth/{provider}/callback'.
        AUTH_OAUTH_GOOGLE (OAuthProviderSettings): Конфигурация Google OAuth-провайдера.

    Конфигурация Pydantic BaseSettings (model_config):
        env_file (Path): путь к .env, полученный через PathSettings.env_path.
        env_file_encoding (str): 'utf-8'.
        env_prefix (str): 'AUTH_'.
        case_sensitive (bool): False.
    """
    # Путь к файлу окружения для AuthSettings
    env_file: str = PathSettings.env_path

    # Базовый URL для auth-эндпоинтов
    AUTH_URL: str = "/api/auth"

    # JWT
    AUTH_TOKEN_TYPE: str = "Bearer"
    AUTH_TOKEN_EXPIRE_MINUTES: int = 1440
    AUTH_VERIFICATION_TOKEN_EXPIRE_MINUTES: int = 1440
    AUTH_TOKEN_ALGORITHM: str = "HS256"
    AUTH_TOKEN_SECRET_KEY: SecretStr
    AUTH_USER_INACTIVE_TIMEOUT: int = 900

    # SMTP
    AUTH_SMTP_SERVER: str = "gmail.smtp"
    AUTH_SMTP_PORT: int = 587
    AUTH_SENDER_EMAIL: str = "noreply@gmail.com"
    AUTH_SMTP_USERNAME: str = "your_username"
    AUTH_SMTP_PASSWORD: SecretStr

    # OAuth
    AUTH_OAUTH_SUCCESS_REDIRECT_URI: AnyUrl
    AUTH_OAUTH_CALLBACK_BASE_URL: AnyUrl
    AUTH_OAUTH_GOOGLE: OAuthProviderSettings

    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file=PathSettings.env_path,
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="AUTH_",
    )
