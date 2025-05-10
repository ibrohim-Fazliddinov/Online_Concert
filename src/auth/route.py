from datetime import datetime

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.routing import  APIRouter, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.constants import AUTH_ACCESS_TOKEN_EXPIRE_MINUTE
from src.auth.dependency import PermissionDependency
from src.auth.permission import IsAuthenticatedPermission, AnonymousPermission
from src.auth.schemas import UserLoginResponse, UserLogin, UserRegisterResponse, UserRegister, UserCreate, UserRead, \
    TokenResponseData
from src.auth.service import UserService
from src.database import get_db_session

user_route = APIRouter()
    # api_route = APIRoute()
@user_route.post(
    "/api/auth/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_u(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db_session),
):
    svc = UserService(session)

    # Проверяем, что email ещё не занят
    if await svc.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    if user_data.phone_number:
        if await svc.get_user_by_phone(user_data.phone_number):
            raise HTTPException(400, "Phone number already exists")

    # Создаём пользователя
    new_user = await svc.create_user(user_data)
    return new_user


@user_route.post("/auth/", response_model=TokenResponseData,)
async def authenticate(
        data: UserLogin,
        session: AsyncSession = Depends(get_db_session),
):
    srv = UserService(session)
    user = await srv.get_user_by_email(email=data.email)
    if user is None:
        raise HTTPException(status_code=404, detail="USER is not registered")

        # Генерируем и возвращаем токен
    access_token = await srv.create_access_token(
        data={"sub": user.email}
    )
    return {
        "success": True,
        "message": "Authenticated successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }

@user_route.post("/auth/logout")
def logout(response: Response):
    """
    Чистим cookie с токеном на клиенте.
    """
    # Удаляем cookie access_token
    response.delete_cookie(key="access_token", path="/")
    return {"msg": "Logged out successfully"}

