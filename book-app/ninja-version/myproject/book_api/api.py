from uuid import UUID

from asgiref.sync import sync_to_async
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
async def get_books(request):
    # all_books = await sync_to_async(list)(Book.objects.all())
    all_books = [book async for book in Book.objects.all()]
    return all_books


@api.post("/books", response={201: BookOut})
async def create_book(request, payload: BookIn):
    # book = await sync_to_async(Book.objects.create)(**payload.dict())
    book = await Book.objects.acreate(**payload.dict())
    return book
