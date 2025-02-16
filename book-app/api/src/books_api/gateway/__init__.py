from abc import ABC, abstractmethod

from sqlmodel import Field, SQLModel


class BookRecord(SQLModel, table=True):
    id: str = Field(primary_key=True)
    isbn: str
    title: str
    page: int

    __tablename__ = "book"


class DatabaseDriver(ABC):
    @abstractmethod
    async def select_books(self) -> list[BookRecord]:
        raise NotImplementedError
