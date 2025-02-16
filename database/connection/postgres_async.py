# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "sqlmodel",
#     "SQLAlchemy[postgresql-asyncpg]",
# ]
# ///

import logging
from pathlib import Path

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession

logging.basicConfig(
    filename=Path(__file__).with_suffix(".log"),
    format="%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


"""Prerequisites:

docker run --rm --name postgres \
    -e POSTGRES_USER=developer \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -e POSTGRES_DB=practice \
    -p 5432:5432 -d postgres:15.10
"""
database_url = "postgresql+asyncpg://developer:mysecretpassword@127.0.0.1:5432/practice"
engine = create_async_engine(database_url)
AsyncSession = async_sessionmaker(engine, class_=SQLModelAsyncSession)


async def main():
    # ref https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    hero_1 = Hero(name="Deadpond (async)", secret_name="Dive Wilson (async)")
    print("Before insert:", hero_1)

    async with AsyncSession.begin() as session:
        session.add(hero_1)
        print("After add:", hero_1)

    print("After session close:", hero_1)
    print()

    print("Heroes:")
    statement = select(Hero)
    async with AsyncSession() as session:
        results = await session.exec(statement)
        for hero in results:
            print(repr(hero))
    print()

    async with AsyncSession() as session:
        # returns SQLAlchemy Row
        results = await session.stream(statement)
        async for row in results:
            print(row[0])


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
