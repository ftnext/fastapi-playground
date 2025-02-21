from typing import Annotated

from fastapi import Depends, FastAPI, status
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession

from books_api.driver.database import PostgresqlDatabaseDriver, get_session
from books_api.gateway.fetch_books import FetchBooksFromDatabase
from books_api.rest.presentations import BookReadModel
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
