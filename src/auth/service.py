from fastapi import HTTPException
from starlette.requests import Request





def decode_jwt_token(token):
    return token

def get_user_by_email(user_email):
    return user_email


def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    payload = decode_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_email = payload.get("email")
    user = get_user_by_email(user_email)  # Функция, которая ищет пользователя в БД

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
