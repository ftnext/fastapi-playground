from books_api.domain.books import Book, Books
from books_api.domain.isbn import ISBN
from books_api.port.fetch_books import FetchBooksPort


class ListBooksUseCase:
    def __init__(self, fetch_books_port: FetchBooksPort) -> None:
        self.fetch_books_port = fetch_books_port

    async def execute(self) -> Books:
        return Books(
            values=[
                Book(
                    id="77a3ed8b-37d4-4602-a808-cb66ffa614c8",
                    isbn=ISBN(value="978-0321125217"),
                    title="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
                    page=320,
                )
            ]
        )
