from books_api.domain.books import Book
from books_api.domain.isbn import ISBN
from books_api.rest.presentations import BookReadModel


class TestBookReadModel:
    def test_create_from_domain_book(self):
        actual = BookReadModel.from_book(
            Book(
                id="07c78602-dd5d-48cc-91dd-24d06b69a56b",
                isbn=ISBN(value="978-3-16-148410-0"),
                title="The Book",
                page=100,
            )
        )

        assert actual == BookReadModel(
            id="07c78602-dd5d-48cc-91dd-24d06b69a56b",
            isbn="978-3-16-148410-0",
            title="The Book",
            page=100,
        )
