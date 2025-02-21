import os

from getgauge.python import after_scenario, before_scenario
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(engine)


class Book(Base):
    __tablename__ = "book"
    id = Column(String, primary_key=True)
    isbn = Column(String)
    title = Column(String)
    page = Column(Integer)


@before_scenario("<load_books>")
def load_books():
    with Session.begin() as session:
        session.add(
            Book(
                id="07c78602-dd5d-48cc-91dd-24d06b69a56b",
                isbn="978-3-16-148410-0",
                title="Book 1",
                page=100,
            )
        )
        session.add(
            Book(
                id="d1489816-bcaf-4453-b64d-a89d3d1564b4",
                isbn="978-3-16-148410-1",
                title="Book 2",
                page=200,
            )
        )


@after_scenario
def delete_books():
    with Session.begin() as session:
        session.query(Book).delete()
