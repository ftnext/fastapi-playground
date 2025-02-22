import uuid

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession

from books_api.config import config
from books_api.gateway import BookRecord, DatabaseDriver


class PostgresqlDatabaseDriver(DatabaseDriver):
    def __init__(self, session: type[SQLModelAsyncSession]):
        self.session = session

    async def select_books(self) -> list[BookRecord]:
        statement = select(BookRecord)
        async with self.session() as session:
            results = await session.exec(statement)
        return [hero for hero in results]

    async def insert_book(self, isbn: str, title: str, page: int) -> None:
        book = BookRecord(id=str(uuid.uuid4()), isbn=isbn, title=title, page=page)
        async with self.session.begin() as session:  # type: ignore[call-arg]
            session.add(book)  # type: ignore[attr-defined]


async_engine = create_async_engine(str(config.pg_dsn))
AsyncSession = async_sessionmaker(async_engine, class_=SQLModelAsyncSession)


# ref: https://github.com/rhoboro/async-fastapi-sqlalchemy/blob/e66ebb385f5330c4c79d6bb9ed836c375a523ea5/app/db.py#L24
async def get_session():
    yield AsyncSession
