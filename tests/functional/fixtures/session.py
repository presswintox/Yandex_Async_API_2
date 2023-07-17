import asyncio

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
