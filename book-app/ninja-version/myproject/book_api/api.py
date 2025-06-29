from uuid import UUID

from ninja import NinjaAPI, Schema

from .models import Book

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    return "Hello world"


class BookIn(Schema):
    isbn: str
    title: str
    page: int


class BookOut(Schema):
    id: UUID
    isbn: str
    title: str
    page: int


@api.get("/books", response=list[BookOut])
def get_books(request):
    books_qs = Book.objects.all()
    return books_qs


@api.post("/books", response={201: BookOut})
async def create_book(request, payload: BookIn):
    book = await Book.objects.acreate(**payload.dict())
    return book
