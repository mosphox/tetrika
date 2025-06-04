import aiohttp
import pytest
from unittest.mock import AsyncMock

from solution.main import fetch


@pytest.mark.asyncio
async def test_fetch_success():
    session = AsyncMock(spec=aiohttp.ClientSession)
    response = AsyncMock()
    response.status = 200
    response.text = AsyncMock(return_value="hello")
    session.get.return_value.__aenter__.return_value = response

    result = await fetch(session, "http://example.com")
    assert result == "hello"
    session.get.assert_called_once()


@pytest.mark.asyncio
async def test_fetch_failure_logs_and_returns_none(caplog):
    session = AsyncMock(spec=aiohttp.ClientSession)
    response = AsyncMock()
    response.status = 404
    response.text = AsyncMock(return_value="not found")
    session.get.return_value.__aenter__.return_value = response

    with caplog.at_level("WARNING"):
        result = await fetch(session, "http://example.com/fail")

    assert result is None
    assert "Failed to fetch" in caplog.text
