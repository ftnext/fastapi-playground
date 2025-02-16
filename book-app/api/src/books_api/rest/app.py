from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello World"}


class BookReadModel(BaseModel):
    id: str = Field(example="77a3ed8b-37d4-4602-a808-cb66ffa614c8")
    isbn: str = Field(examples=["978-0321125217"])
    title: str = Field(
        examples=["Domain-Driven Design: Tackling Complexity in the Heart of Softwares"]
    )
    page: int = Field(ge=0, examples=[320])
    read_page: int = Field(ge=0, examples=[120])
    created_at: int = Field(examples=[1136214245000])
    updated_at: int = Field(examples=[1136214245000])


@app.get("/books", response_model=list[BookReadModel], status_code=status.HTTP_200_OK)
async def get_books():
    book = BookReadModel(
        id="77a3ed8b-37d4-4602-a808-cb66ffa614c8",
        isbn="978-0321125217",
        title="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
        page=320,
        read_page=120,
        created_at=1136214245000,
        updated_at=1136214245000,
    )
    return [book]
