from fastapi import Depends, FastAPI, status
from pydantic import BaseModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession

from books_api.domain.books import Book
from books_api.driver.database import PostgresqlDatabaseDriver, get_session
from books_api.gateway.fetch_books import FetchBooksFromDatabase
from books_api.port.fetch_books import FetchBooksPort
from books_api.use_case.list_books import ListBooksUseCase

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello World"}


class BookReadModel(BaseModel):
    id: str = Field(example="77a3ed8b-37d4-4602-a808-cb66ffa614c8")
    isbn: str = Field(examples=["978-0321125217"])
    title: str = Field(
        examples=["Domain-Driven Design: Tackling Complexity in the Heart of Softwares"]
    )
    page: int = Field(ge=0, examples=[320])

    @classmethod
    def from_book(cls, book: Book) -> "BookReadModel":
        return cls(
            id=book.id,
            isbn=book.isbn.value,
            title=book.title,
            page=book.page,
        )


def get_books_deps(
    session: type[SQLModelAsyncSession] = Depends(get_session),
) -> FetchBooksPort:
    return FetchBooksFromDatabase(PostgresqlDatabaseDriver(session))


@app.get("/books", response_model=list[BookReadModel], status_code=status.HTTP_200_OK)
async def get_books(fetch_books_port: FetchBooksPort = Depends(get_books_deps)):
    use_case = ListBooksUseCase(fetch_books_port)
    books = await use_case.execute()
    return [BookReadModel.from_book(book) for book in books]
