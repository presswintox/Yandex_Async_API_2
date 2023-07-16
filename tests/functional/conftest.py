import asyncio
import json
from typing import List

import aiohttp
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from redis.asyncio.client import Redis

from tests.functional.settings import test_settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    redis = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    await redis.flushall()
    yield redis
    await redis.close()


@pytest_asyncio.fixture(scope='session')
async def es_client():
    es_url = f'http://{test_settings.es_host}' \
             f':{test_settings.es_port}'
    client = AsyncElasticsearch(hosts=[es_url])
    yield client
    await client.close()


@pytest.fixture()
def redis_write_data(redis_client):
    async def inner(index, query, data: List[dict]):
        query = dict_to_query_string(query)
        await redis_client.set(f'{index}:{query}', json.dumps(data), 60)

    return inner


@pytest.fixture()
def es_write_data(es_client):
    async def inner(index, data: List[dict]):
        bulk_query = []
        for row in data:
            bulk_query.append(
                {'index': {'_index': index,
                           '_id': row['id']}})
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
        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)

        await es_client.indices.create(
            index=index,
            settings=body['settings'],
            mappings=body['mappings']
        )

    return inner


def dict_to_query_string(data: dict) -> str:
    if not data.get('page_size'):
        data['page_size'] = 50
    if not data.get('page_number'):
        data['page_number'] = 1
    return '&'.join([f'{key}={value}' for key, value in data.items()])
