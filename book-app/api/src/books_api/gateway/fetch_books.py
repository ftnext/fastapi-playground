from books_api.domain.books import Book, Books
from books_api.domain.isbn import ISBN
from books_api.gateway import BookRecord, DatabaseDriver
from books_api.port.fetch_books import FetchBooksPort


def books_from_records(book_records: list[BookRecord]) -> Books:
    return Books(
        values=[
            Book(
                id=book_record.id,
                isbn=ISBN(value=book_record.isbn),
                title=book_record.title,
                page=book_record.page,
            )
            for book_record in book_records
        ]
    )


Books.from_ = staticmethod(books_from_records)  # type: ignore[attr-defined]


class FetchBooksFromDatabase(FetchBooksPort):
    def __init__(self, database: DatabaseDriver):
        self.database = database

    async def fetch(self) -> Books:
        book_records = await self.database.select_books()
        return Books.from_(book_records)  # type: ignore[attr-defined]
