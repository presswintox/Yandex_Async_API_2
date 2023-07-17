import json
from typing import List

import pytest


@pytest.fixture()
def redis_write_data(redis_client):
    async def inner(index, query, data: List[dict]):
        query = dict_to_query_string(query)
        await redis_client.set(f'{index}:{query}', json.dumps(data), 60)

    return inner

def dict_to_query_string(data: dict) -> str:
    if not data.get('page_size'):
        data['page_size'] = 50
    if not data.get('page_number'):
        data['page_number'] = 1
    return '&'.join([f'{key}={value}' for key, value in data.items()])
