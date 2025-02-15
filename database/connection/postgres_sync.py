# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "sqlmodel",
#     "SQLAlchemy[postgresql]",
# ]
# ///
# Based on: https://gist.github.com/ftnext/a15376f38433ffeb5c613d5e76b4ee61
import logging
from pathlib import Path

from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel, create_engine

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
database_url = "postgresql://developer:mysecretpassword@127.0.0.1:5432/practice"
engine = create_engine(database_url)
Session = sessionmaker(engine)

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    print("Before insert:", hero_1)
    # Before insert: name='Deadpond' secret_name='Dive Wilson' id=None age=None

    with Session.begin() as session:  # transaction
        session.add(hero_1)
        print("After add:", hero_1)
        # After add: name='Deadpond' secret_name='Dive Wilson' id=None age=None

        session.commit()  # Close the session
        print("After commit:", hero_1)
        # After commit:

    print("After session close:", hero_1)
    # After session close:
