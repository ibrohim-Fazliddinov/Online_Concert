from fastapi.params import Depends
from fastapi.routing import APIRoute, APIRouter

from src.auth.dependency import PermissionDependency
from src.auth.permission import AnonymousPermission
from src.auth.schemas import UserLoginResponse, UserLogin
from src.auth.security import AuthSecurity
from src.auth.service import UserService

user_route = APIRouter()
    # api_route = APIRoute()


@user_route.post("api/login", dependencies=[
    Depends(PermissionDependency([AnonymousPermission]))
], response_model=UserLoginResponse,
)
async def login(
        data: UserLogin,
        auth: AuthSecurity = Depends()
):
    result = await auth.login(data.email, data.password)
    return result

