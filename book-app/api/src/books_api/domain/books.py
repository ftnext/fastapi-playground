from collections.abc import Generator

from pydantic import BaseModel

from books_api.domain.isbn import ISBN


class Book(BaseModel, frozen=True):
    id: str
    isbn: ISBN
    title: str
    page: int


class Books(BaseModel):
    values: list[Book]

    def __iter__(self) -> Generator[Book, None, None]:  # type: ignore[override]
        yield from self.values
