import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.asyncio
async def test_fetch_pages_yields_data():
    """Verify the generator yields the expected number of pages."""
    pages = []
    with patch('aiohttp.ClientSession') as mock_session_class:
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=[{"price": 10}, {"price": 20}])
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session

        from python_async_generator import fetch_pages
        async for page in fetch_pages("https://api.example.com/items", 30, page_size=10):
            pages.append(page)
            if len(pages) >= 3:
                break
    assert len(pages) == 3
    assert all(isinstance(p, list) for p in pages)


@pytest.mark.asyncio
async def test_generator_stops_on_empty_data():
    """Verify the generator stops when the API returns empty data."""
    with patch('aiohttp.ClientSession') as mock_session_class:
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=[])
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session

        from python_async_generator import fetch_pages
        pages = []
        async for page in fetch_pages("https://api.example.com/items", 100):
            pages.append(page)
    assert len(pages) == 0


@pytest.mark.asyncio
async def test_early_exit_closes_generator():
    """Verify that breaking early and calling aclose() works."""
    with patch('aiohttp.ClientSession') as mock_session_class:
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=[{"price": 10}])
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session

        from python_async_generator import fetch_pages
        gen = fetch_pages("https://api.example.com/items", 10000)
        async for _ in gen:
            break
        await gen.aclose()
        # No exception means cleanup ran successfully
