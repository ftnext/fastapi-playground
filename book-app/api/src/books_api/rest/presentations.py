from pydantic import BaseModel, Field

from books_api.domain.books import Book


class BookReadModel(BaseModel):
    id: str = Field(examples=["77a3ed8b-37d4-4602-a808-cb66ffa614c8"])
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
