import aiohttp
import pytest


@pytest.fixture()
def make_get_request():
    async def inner(url, params=None):
        session = aiohttp.ClientSession()
        async with session.get(url, params=params) as response:
            body = await response.json()
            status = response.status
        await session.close()
        return body, status

    return inner

