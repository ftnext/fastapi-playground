from books_api.domain.books import Books
from books_api.port.fetch_books import FetchBooksPort


class ListBooksUseCase:
    def __init__(self, fetch_books_port: FetchBooksPort) -> None:
        self.fetch_books_port = fetch_books_port

    async def execute(self) -> Books:
        return await self.fetch_books_port.fetch()
