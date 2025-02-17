from fastapi import Depends, FastAPI, status
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession

from books_api.driver.database import PostgresqlDatabaseDriver, get_session
from books_api.gateway.fetch_books import FetchBooksFromDatabase
from books_api.port.fetch_books import FetchBooksPort
from books_api.rest.presentations import BookReadModel
from books_api.use_case.list_books import ListBooksUseCase

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello World"}


def get_books_deps(
    session: type[SQLModelAsyncSession] = Depends(get_session),
) -> FetchBooksPort:
    return FetchBooksFromDatabase(PostgresqlDatabaseDriver(session))


@app.get("/books", response_model=list[BookReadModel], status_code=status.HTTP_200_OK)
async def get_books(fetch_books_port: FetchBooksPort = Depends(get_books_deps)):
    use_case = ListBooksUseCase(fetch_books_port)
    books = await use_case.execute()
    return [BookReadModel.from_book(book) for book in books]
