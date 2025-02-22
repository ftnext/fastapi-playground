from abc import ABC, abstractmethod

from books_api.domain.isbn import ISBN


class StoreBookPort(ABC):
    @abstractmethod
    async def store(self, isbn: ISBN, title: str, page: int) -> None:
        raise NotImplementedError
