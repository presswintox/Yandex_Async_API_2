import datetime
import uuid
import json

import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings


#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`, который следит за запуском и работой цикла событий.

@pytest.mark.asyncio
async def test_search(es_write_data):
    # 1. Генерируем данные для ES

    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': [{'id': '97f168bd-d10d-481b-ad38-89d252a13feb3', 'full_name': 'Ben'},
            {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name': 'Howard'}],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name': 'Ann'},
            {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name': 'Bob'}
        ],
        'writers': [
            {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name': 'Ben'},
            {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name': 'Howard'}
        ],
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat(),
        'film_work_type': 'movie'
    } for _ in range(60)]

    await es_write_data(es_data)

    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/films/search'
    query_data = {'query': 'The Star'}
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    # 4. Проверяем ответ

    assert status == 200
    print(body)
    assert len(body) == 50
