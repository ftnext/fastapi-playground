from books_api.domain.isbn import ISBN
from books_api.gateway import DatabaseDriver
from books_api.port.store_book_port import StoreBookPort


class StoreBookInDatabase(StoreBookPort):
    def __init__(self, driver: DatabaseDriver) -> None:
        self.driver = driver

    async def store(self, isbn: ISBN, title: str, page: int) -> None:
        await self.driver.insert_book(isbn.value, title, page)
