from books_api.domain.isbn import ISBN
from books_api.port.store_book_port import StoreBookPort


class CreateBookUseCase:
    def __init__(self, store_book_port: StoreBookPort) -> None:
        self.store_book_port = store_book_port

    async def execute(self, isbn: ISBN, title: str, page: int) -> None:
        await self.store_book_port.store(isbn, title, page)
