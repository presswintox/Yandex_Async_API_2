from typing import List

import pytest


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
