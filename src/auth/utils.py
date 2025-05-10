"""
utils.py

Модуль содержит утилиты для работы с паролями:
    - hash_password: хеширует пароль с использованием bcrypt.
    - generate_password: генерирует случайный пароль заданной длины по критериям безопасности.

Пример использования:

    from src.common.password_utils import hash_password, generate_password

    # Хеширование пароля
    hashed = hash_password("MySecret123")
    print(hashed)

    # Генерация случайного пароля
    pwd = generate_password()
    print(pwd)
"""

import secrets
import string
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def generate_password():
    """
    Генерирует случайный пароль, соответствующий критериям безопасности:
      - Длина: 10 символов.
      - Минимум одна строчная буква.
      - Минимум одна заглавная буква.
      - Минимум три цифры.

    Пароль состоит из букв латинского алфавита и цифр.
    Функция повторяет генерацию, пока не выполняются все условия.

    Возвращает:
    - str: Сгенерированная строка пароля.

    Пример:
    >>> pwd = generate_password()
    >>> len(pwd) == 10
    True
    >>> sum(c.isdigit() for c in pwd) >= 3
    True
    """
    alphanumeric = string.ascii_letters + string.digits
    while True:
        password = "".join(secrets.choice(alphanumeric) for i in range(10))
        if (
            any(c.lower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >=3
        ):
            break
    return password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Сравнивает plain-пароль с его хэшем.
    Возвращает True, если они совпадают.
    """
    return pwd_context.verify(plain_password, hashed_password)



