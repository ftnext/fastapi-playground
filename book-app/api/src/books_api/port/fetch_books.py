from abc import ABC, abstractmethod

from books_api.domain.books import Books


class FetchBooksPort(ABC):
    @abstractmethod
    async def fetch(self) -> Books:
        raise NotImplementedError
