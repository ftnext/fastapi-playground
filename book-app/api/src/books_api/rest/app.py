from typing import Annotated

from fastapi import Depends, FastAPI, status
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession

from books_api.domain.isbn import ISBN
from books_api.driver.database import PostgresqlDatabaseDriver, get_session
from books_api.gateway.fetch_books import FetchBooksFromDatabase
from books_api.gateway.store_book import StoreBookInDatabase
from books_api.rest.presentations import BookCreateRequest, BookReadModel
from books_api.use_case.create_book import CreateBookUseCase
from books_api.use_case.list_books import ListBooksUseCase

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello World"}


def inject_list_books_use_case(
    session: Annotated[type[SQLModelAsyncSession], Depends(get_session)],
) -> ListBooksUseCase:
    return ListBooksUseCase(FetchBooksFromDatabase(PostgresqlDatabaseDriver(session)))


@app.get("/books", response_model=list[BookReadModel], status_code=status.HTTP_200_OK)
async def get_books(
    use_case: Annotated[ListBooksUseCase, Depends(inject_list_books_use_case)],
):
    books = await use_case.execute()
    return [BookReadModel.from_book(book) for book in books]


def inject_create_book_use_case(
    session: Annotated[type[SQLModelAsyncSession], Depends(get_session)],
) -> CreateBookUseCase:
    return CreateBookUseCase(StoreBookInDatabase(PostgresqlDatabaseDriver(session)))


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(
    request: BookCreateRequest,
    use_case: Annotated[CreateBookUseCase, Depends(inject_create_book_use_case)],
) -> None:
    await use_case.execute(ISBN(value=request.isbn), request.title, request.page)
