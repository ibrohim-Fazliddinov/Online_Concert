"""
permissions.py

Модуль содержит абстрактные классы для проверки прав доступа пользователей.
Предоставляет:
    - BasePermission: базовый класс для определения логики проверки прав.
    - AdminUserPermission: проверка роли администратора.
    - ManagerUserPermission: проверка роли менеджера.
    - CustomerUserPermission: проверка роли клиента.
    - AnonymousPermission: проверка анонимного доступа.

Пример использования:
```python
from src.permissions import AdminUserPermission
from starlette.requests import Request

# В обработчике FastAPI
async def protected_endpoint(request: Request):
    # Выбросит HTTPException, если текущий пользователь не администратор
    AdminUserPermission(request)
    return {"detail": "Доступ разрешён"}
```
"""
from abc import ABC, abstractmethod
from fastapi import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from src.auth.enum import UserRoles
from src.auth.security import AuthSecurity


class BasePermission(ABC):
    """
    Абстрактный базовый класс для проверки прав доступа пользователей.

    Атрибуты:
        error_message (list): Сообщение об ошибке при отсутствии прав.
        error_code (int): HTTP-код ошибки при отсутствии прав.
        role (UserRoles | None): Роль пользователя для проверки прав.
    """
    error_message = [{"msg": "У вас нет прав для выполнения этого действия"}]
    error_code = HTTP_403_FORBIDDEN

    role = None

    @abstractmethod
    def has_required_permission(self, request: Request) -> bool:
        """
        Проверяет, соответствует ли роль текущего пользователя требуемой для доступа.

        Args:
            request (Request): объект HTTP-запроса.

        Returns:
            bool: True, если у пользователя есть необходимые права, иначе False.
        """
        pass

    def __init__(self, request: Request):
        """
        Инициализация проверки прав для текущего пользователя.

        Извлекает пользователя из запроса и проверяет, имеет ли он требуемую роль.
        В случае отсутствия прав вызывает HTTPException с кодом и сообщением об ошибке.

        Args:
            request (Request): объект HTTP-запроса.

        Raises:
            HTTPException: если пользователь не имеет необходимых прав.
        """
        self.user = AuthSecurity.get_current_user(request)

        if not self.has_required_permission(request):
            raise HTTPException(status_code=self.error_code, detail=self.error_message)


class AdminUserPermission(BasePermission):
    """
    Проверяет, является ли текущий пользователь администратором.
    """

    def has_required_permission(self, request: Request) -> bool:
        """
        Возвращает True, если роль пользователя == UserRoles.admin.
        """
        return self.user and self.user.role == UserRoles.admin


class ManagerUserPermission(BasePermission):
    """
    Проверяет, является ли текущий пользователь менеджером.
    """

    def has_required_permission(self, request: Request) -> bool:
        """
        Возвращает True, если роль пользователя == UserRoles.manager.
        """
        return self.user and self.user.role == UserRoles.manager


class CustomerUserPermission(BasePermission):
    """
    Проверяет, является ли текущий пользователь клиентом.
    """

    def has_required_permission(self, request: Request) -> bool:
        """
        Возвращает True, если роль пользователя == UserRoles.client.
        """
        return self.user and self.user.role == UserRoles.client


class AnonymousPermission(BasePermission):
    """
    Разрешает доступ только анонимным (неавторизованным) пользователям.
    """

    def has_required_permission(self, request: Request) -> bool:
        """
        Возвращает True, если пользователь не прошёл аутентификацию.
        """
        return self.user is None
