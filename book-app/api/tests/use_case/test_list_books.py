from unittest.mock import AsyncMock

import pytest

from books_api.port.fetch_books import FetchBooksPort
from books_api.use_case.list_books import ListBooksUseCase


@pytest.mark.asyncio
async def test_execute():
    port = AsyncMock(spec=FetchBooksPort)
    sut = ListBooksUseCase(port)

    actual = await sut.execute()

    assert actual == port.fetch.return_value
    port.fetch.assert_awaited_once()
