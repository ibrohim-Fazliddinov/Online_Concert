from typing import Optional
import jwt
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose.exceptions import JWTError
from sqlalchemy.orm import Session
from src.auth.enum import UserRoles
from src.auth.exception import credentials_exception
from src.auth.schemas import UserBase, UserRegister, UserCreate
import logging

log = logging.getLogger(__name__)


def get_user_by_email(*, db_session, email: str) -> Optional[UserBase]:
    """Возвращает пользователя по email или None, если не найден."""
    return db_session.query(UserBase).filter(UserBase.email == email).one_or_none()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = None
ALGORITHM = None
def verify_token(token: str) -> str:
    """Декодирует JWT и возвращает email из payload.sub."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise JWTError()
        return email
    except JWTError as e:
        log.warning("JWT decode failed: %s", e)
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserBase:
    email = verify_token(token)
    user = get_user_by_email(db_session=db, email=email)
    if not user:
        raise credentials_exception
    return user



def create_u(*, db_session, user_in: (UserRegister | UserCreate)) -> UserBase:
    password = bytes(user_in.password, 'utf-8')

    user = UserBase(
        **user_in.model_dump(exclude={"password", "role"}), password=password
    )

    role = UserRoles.client
    if hasattr(user_in, "role"):
        role = user_in.role

    db_session.add(user)
    db_session.commit()
    return user