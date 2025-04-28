from abc import ABC, abstractmethod
from fastapi import HTTPException
from starlette.requests import Request

from rest_framework.status import HTTP_403_FORBIDDEN

from src.auth.enum import UserRoles
from src.auth.service import get_current_user


class BasePermission(ABC):
    error_message = [{"msg": "You don't have permission to perform this action"}]
    error_code = HTTP_403_FORBIDDEN

    role = None

    @abstractmethod
    def has_required_permission(self, request: Request) -> bool:
        pass


    def __init__(self, request: Request):
        self.user = get_current_user(request)

        if not self.has_required_permission(request):
            raise HTTPException(status_code=self.error_code, detail=self.error_message)


class AdminUserPermission(BasePermission):

    def has_required_permission(self, request: Request):
        return self.role == UserRoles.admin

class ManagerUserPermission(BasePermission):

    def has_required_permission(self, request: Request):
        return self.role == UserRoles.manager


class CustomerUserPermission(BasePermission):

    def has_required_permission(self, request: Request):
        return self.role == UserRoles.client

class AnonymousPermission(BasePermission):
    def has_required_permission(self, request: Request) -> bool:
        return self.user is None
