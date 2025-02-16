from books_api.domain.books import Book
from books_api.domain.isbn import ISBN
from books_api.gateway import BookRecord
from books_api.gateway.fetch_books import Books


def test_create_books_from_records():
    actual = Books.from_(
        [
            BookRecord(
                id="07c78602-dd5d-48cc-91dd-24d06b69a56b",
                isbn="978-3-16-148410-0",
                title="Book 1",
                page=100,
            ),
            BookRecord(
                id="d1489816-bcaf-4453-b64d-a89d3d1564b4",
                isbn="978-3-16-148410-1",
                title="Book 2",
                page=200,
            ),
        ]
    )

    assert actual == Books(
        values=[
            Book(
                id="07c78602-dd5d-48cc-91dd-24d06b69a56b",
                isbn=ISBN(value="978-3-16-148410-0"),
                title="Book 1",
                page=100,
            ),
            Book(
                id="d1489816-bcaf-4453-b64d-a89d3d1564b4",
                isbn=ISBN(value="978-3-16-148410-1"),
                title="Book 2",
                page=200,
            ),
        ]
    )
