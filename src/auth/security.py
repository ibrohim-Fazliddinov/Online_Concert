from settings import logging
import os
from datetime import datetime, timedelta

import bcrypt
import jwt
from jose.exceptions import JWTError

from src.auth.exception import credentials_exception

log = logging.getLogger(__name__)

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS356"
ACCESS_TOKEN_URL = 24


class HashingMixin:
    @classmethod
    def hash_password(password: str):
        """
        Генерирует хешированную версию переданного пароля с использованием алгоритма bcrypt.

        Эта функция выполняет хеширование пароля с добавлением случайной соли для обеспечения
        безопасности хранения паролей в базе данных. Хеширование позволяет избежать хранения
        паролей в открытом виде, что повышает безопасность приложения.

        Процесс хеширования включает два основных шага:
        1. Преобразование пароля в байты с использованием кодировки UTF-8.
        2. Генерация уникальной соли с помощью `bcrypt.gensalt()`, которая используется в
           комбинации с паролем для создания хеша.

        Важно:
        - Соль гарантирует, что даже одинаковые пароли будут иметь уникальные хеши.
        - bcrypt — это алгоритм хеширования, специально спроектированный для защиты паролей,
          который добавляет защиту от атак с использованием радужных таблиц и брутфорса.

        Аргументы:
        - password (str): Строка, представляющая пароль, который нужно захешировать.

        Возвращает:
        - bytes: Хешированный пароль в виде байтов, который можно безопасно хранить в базе данных.

        Пример:
        >>> hashed_password = hash_password("MyPassword123")
        >>> print(hashed_password)
        b'$2b$12$A8h9p1g4KZBO7seG8oOsLeF/jEzq7VzYAe6b2FV8gG3A8bTtCw1hC'

        Почему используется:
        - Преобразование пароля в байты (с помощью `bytes(password, "utf-8")`) необходимо,
          потому что алгоритмы хеширования требуют ввода в виде байтов, а не строк.
        - Соль генерируется с помощью `bcrypt.gensalt()`, что позволяет избежать атак с использованием
          радужных таблиц, где заранее вычисляются хеши для часто используемых паролей.
        - Использование `bcrypt.hashpw()` обеспечивает безопасное хеширование пароля с солью, делая его
          уникальным и стойким к большинству атак.
        """
        # Преобразуем строковый пароль в байты для использования с bcrypt
        pw = bytes(password, "utf-8")

        # Генерируем соль для обеспечения уникальности хешей
        salt = bcrypt.gensalt()

        # Хешируем пароль с солью и возвращаем хеш
        return bcrypt.hashpw(pw, salt)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: bytes) -> bool:
        if not plain_password or not hashed_password:
            return False
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)

def verify_token(token: str) -> str:
    """Декодирует JWT и возвращает email из payload.sub."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        log.warning("JWT decode failed: %s", e)
        raise credentials_exception
    sub = payload.get('sub')
    if sub is None:
        raise credentials_exception
    return sub

def create_access_token(subject: str) -> str:
    now = datetime.utcnow()
    expire = now + timedelta(hours=ACCESS_TOKEN_URL)
    to_encode = {"sub": subject, "exp": expire}
    if not SECRET_KEY:
        raise RuntimeError("")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

