from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello World!"}


if __name__ == "__main__":
    import logging

    sqlalchemy_logger = logging.getLogger("sqlalchemy")
    sqlalchemy_logger.setLevel(logging.INFO)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    )
    sqlalchemy_logger.addHandler(stdout_handler)

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.commit()
