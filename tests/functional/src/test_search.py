import uuid

import pytest
from elasticsearch import AsyncElasticsearch

from elasticbuild.pyfiles.moviessettings import ES_SCHEMA
from tests.functional.settings import test_settings
from tests.functional.conftest import es_client, elas_init_index


#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`, который следит за запуском и работой цикла событий.

@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'The Star'},
                {'status': 200, 'length': 50}
        ),
        (
                {'query': 'Mashed potato'},
                {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(es_write_data, make_get_request, elas_init_index,
                      query_data: dict,
                      expected_answer: dict):
    # 1. Генерируем данные для ES

    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': [{'id': '97f168bd-d10d-481b-ad38-89d252a13feb',
                   'name': 'Ben'},
                  {'id': '97f168bd-d10d-481b-ad38-89d252a13feb',
                   'name': 'Howard'}],
        'title': 'The Star',
        'description': 'New World',
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name': 'Ann'},
            {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name': 'Bob'}
        ],
        'writers': [
            {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name': 'Ben'},
            {'id': '97f168bd-d10d-481b-ad38-89d252a13feb',
             'full_name': 'Howard'}
        ],
        'directors': [
            {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name':
                'Stan'},
            {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name':
                'Howard'}
        ]
    } for _ in range(60)]
    await elas_init_index('movies', ES_SCHEMA)
    await es_write_data(es_data)
    response, status = await make_get_request(url=test_settings.service_url +
                                              '/api/v1/films/search',
                                              params=query_data)

    assert status == expected_answer['status']
    assert len(response) == expected_answer['length']
