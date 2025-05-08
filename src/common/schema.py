from pydantic.types import conint, constr
from pydantic import BaseModel, ConfigDict

PrimaryKey = conint(gt=0, lt=2147483647)
NameStr = constr(regex=r"^(?!\s*$).+", strip_whitespace=True, min_length=3)


class ConcertBase(BaseModel):
    """
    Базовая модель для всех Pydantic моделей.
    Используется для наследования общих настроек для всех моделей, таких как валидация при присваивании
    значений и поддержка работы с ORM (например, SQLAlchemy).
    """

    model_config = ConfigDict(
        from_attributes=True,  # Разрешает использование атрибутов модели для создания экземпляра | вместо orm_mode:
        validate_assignment=True,  # Включает валидацию при присваивании значений
        arbitrary_types_allowed=True,  # Разрешает использование произвольных типов данных
    )

class Pagination(ConcertBase):
    """
    Модель для пагинации.
    Используется для определения структуры данных, связанных с пагинацией в API,
    включая количество элементов на странице, текущую страницу и общее количество элементов.
    """

    itemsPerPage: int  # Количество элементов на одной странице.
    page: int  # Номер текущей страницы.
    total: int  # Общее количество элементов в системе.
