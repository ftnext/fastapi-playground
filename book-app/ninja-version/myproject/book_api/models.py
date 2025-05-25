import uuid
from django.db import models


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn = models.CharField(max_length=17, unique=True)
    title = models.CharField(max_length=255)
    page = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} ({self.isbn})"

    class Meta:
        db_table = "book"
