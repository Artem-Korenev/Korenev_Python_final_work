from pydantic import BaseModel, Field, field_validator
from .books import ReturnedBook

# from pydantic_core import PydanticCustomError

__all__ = [
    "IncomingSeller",
    "ReturnedSeller",
    "ReturnedAllSellers",
    "ReturnedSellerWithBooks",
]


# Базовый класс "Книги", содержащий поля, которые есть во всех классах-наследниках.
class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    e_mail: str


# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingSeller(BaseSeller):
    password: str


# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedSeller(BaseSeller):
    id: int


# Класс для возврата массива объектов "Книга"
class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]


class ReturnedSellerWithBooks(ReturnedSeller):
    id: int
    books: list[ReturnedBook]
