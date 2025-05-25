from ninja import NinjaAPI, Schema

from .models import Book

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    return "Hello world"


class BookOut(Schema):
    id: str
    isbn: str
    title: str
    page: int


@api.get("/books", response=list[BookOut])
def get_books(request):
    books_qs = Book.objects.all()
    return books_qs
