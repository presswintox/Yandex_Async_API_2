import asyncio
from typing import List

import aiohttp
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from redis.asyncio.client import Redis

from functional.settings import test_settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def redis_cleaner():
    redis = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    await redis.flushall()

    await redis.close()


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch('http://127.0.0.1:9200')
    yield client
    await client.close()


@pytest.fixture()
def es_write_data(es_client):
    async def inner(data: List[dict]):
        bulk_query = []
        for row in data:
            bulk_query.append(
                {'index': {'_index': test_settings.es_index,
                           '_id': row[test_settings.es_id_field]}})
            bulk_query.append(row)

        response = await es_client.bulk(operations=bulk_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


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


@pytest.fixture()
def elas_init_index(es_client):
    async def inner(index: str, body: dict):
        await es_client.indices.delete(index=index, ignore=[400, 404])
        await es_client.indices.create(
            index=index,
            ignore=400,
            body=body
        )

    return inner
