from typing import List

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch

from functional.settings import test_settings


@pytest.fixture
def es_write_data(es_client):
    async def inner(data: List[dict]):
        bulk_query = []
        for row in data:
            bulk_query.append(
                {'index': {'_index': test_settings.es_index,
                           '_id': row[test_settings.es_id_field]}})
            bulk_query.append(row)

        # bulk_query = get_es_bulk_query(data, test_settings.es_index,
        #                                test_settings.es_id_field)
        # str_query = '\n'.join(bulk_query) + '\n'
        response = await es_client.bulk(operations=bulk_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='127.0.0.1:9200')
    yield client
    await client.close()


@pytest.fixture
def make_get_request(url, params=None):
    async def inner():
        session = aiohttp.ClientSession()
        async with session.get(url, params=params) as response:
            body = await response.json()
            status = response.status
        await session.close()
        return status, body

    return inner
