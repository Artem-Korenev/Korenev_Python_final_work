from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from src.models.sellers import Seller
from src.models.books import Book
from icecream import ic


from src.schemas import (
    IncomingSeller,
    ReturnedAllSellers,
    ReturnedSeller,
    ReturnedSellerWithBooks,
)

from icecream import ic
from sqlalchemy.ext.asyncio import AsyncSession
from src.configurations import get_async_session

sellers_router = APIRouter(tags=["sellers"], prefix="/sellers")

# CRUD - Create, Read, Update, Delete

DBSession = Annotated[AsyncSession, Depends(get_async_session)]


# Ручка для создания записи о книге в БД. Возвращает созданную книгу.
# @books_router.post("/books/", status_code=status.HTTP_201_CREATED)
@sellers_router.post(
    "/", response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED
)  # Прописываем модель ответа
async def create_seller(
    seller: IncomingSeller,
    session: DBSession,
):  # прописываем модель валидирующую входные данные
    # session = get_async_session() вместо этого мы используем иньекцию зависимостей DBSession

    # это - бизнес логика. Обрабатываем данные, сохраняем, преобразуем и т.д.
    new_seller = Seller(
        **{
            "first_name": seller.first_name,
            "last_name": seller.last_name,
            "e_mail": seller.e_mail,
            "password": seller.password,
        }
    )

    session.add(new_seller)
    await session.flush()

    return new_seller


# Ручка, возвращающая все книги
@sellers_router.get("/", response_model=ReturnedAllSellers)
async def get_all_sellers(session: DBSession):
    # Хотим видеть формат
    # books: [{"id": 1, "title": "blabla", ...., "year": 2023},{...}]
    query = select(Seller)  # SELECT * FROM book
    result = await session.execute(query)
    sellers = result.scalars().all()
    return {"sellers": sellers}


# # Ручка для получения книги по ее ИД
# @sellers_router.get("/{id}", response_model=ReturnedSeller)
# async def get_seller(id: int, session: DBSession):
#     if result := await session.get(Seller, id):

#         return result

#     return Response(status_code=status.HTTP_404_NOT_FOUND)


# Ручка для получения книги по ее ИД
@sellers_router.get("/{id}", response_model=ReturnedSellerWithBooks)
async def get_seller(id: int, session: DBSession):
    if result := await session.get(Seller, id):
        ic(result)
        query = select(Book).where(Book.seller_id == id)  # SELECT * FROM book
        result1 = await session.execute(query)
        books = result1.scalars().all()
        ic(books)
        ic(type(result))
        return result

        # books = await session.execute(select(Book).where(Book.seller_id == id))
        # books = books.scalars().all()
        # h = {"books": books}
        # ic(h)
        # {"books": books}
        # returned_seller = ReturnedSeller.from_orm(seller)
        # returned_books = [ReturnedBook.from_orm(book) for book in books]

        # response_data = {**result.dict(), "books": books}

        # return response_data

    return Response(status_code=status.HTTP_404_NOT_FOUND)

    # Получаем книги, связанные с этим продавцом

    # # Формируем ответ
    # returned_seller = ReturnedSeller.from_orm(seller)
    # returned_books = [ReturnedBook.from_orm(book) for book in books]


# Ручка для удаления книги
@sellers_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(id: int, session: DBSession):
    deleted_seller = await session.get(Seller, id)
    ic(
        deleted_seller
    )  # Красивая и информативная замена для print. Полезна при отладке.
    if deleted_seller:
        await session.delete(deleted_seller)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


# Ручка для обновления данных о книге
@sellers_router.put("/{book_id}", response_model=ReturnedSeller)
async def update_book(
    book_id: int, new_seller_data: ReturnedSeller, session: DBSession
):
    # Оператор "морж", позволяющий одновременно и присвоить значение и проверить его. Заменяет то, что закомментировано выше.
    if updated_seller := await session.get(Seller, book_id):
        updated_seller.first_name = new_seller_data.first_name
        updated_seller.last_name = new_seller_data.last_name
        updated_seller.e_mail = new_seller_data.e_mail

        await session.flush()

        return updated_seller

    return Response(status_code=status.HTTP_404_NOT_FOUND)
