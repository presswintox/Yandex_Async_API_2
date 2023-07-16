import pytest

from elasticbuild.pyfiles.moviessettings import ES_SCHEMA
from tests.functional.testdata.init_data import FILMS_DATA
from tests.functional.settings import test_settings

URL_SEARCH = test_settings.service_url + '/api/v1/films/search'
INDEX = 'movies'


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {},
            {'status': 200, 'length': 10}
        ),
        (
                {'query': 'The Star'},
                {'status': 200, 'length': 10}
        ),
        (
                {'query': 'Mashed potato'},
                {'status': 200, 'length': 0}
        ),
        (
                {'query': 'The Star', 'page_size': 5, 'page_number': 1},
                {'status': 200, 'length': 5}
        ),
        (
                {'query': 'The Star', 'sort': '123123'},
                {'status': 400, 'length': 1}
        ),
        (
                {'query': '23423423084u0hj045u60'},
                {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(es_write_data,
                      make_get_request,
                      elas_init_index,
                      query_data: dict,
                      expected_answer: dict):
    await elas_init_index(INDEX, ES_SCHEMA)
    await es_write_data(INDEX, FILMS_DATA)
    response, status = await make_get_request(url=URL_SEARCH,
                                              params=query_data)

    assert status == expected_answer['status']
    assert len(response) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'The Star', 'page_size': 5, 'page_number': 1},
                {'status': 200, 'length': 5}
        )
    ]
)
@pytest.mark.asyncio
async def test_search_with_redis(redis_write_data,
                                 make_get_request,
                                 query_data: dict,
                                 expected_answer: dict):
    await redis_write_data(INDEX, query_data, FILMS_DATA)
    response, status = await make_get_request(url=URL_SEARCH,
                                              params=query_data)

    assert status == expected_answer['status']
    assert len(response) == expected_answer['length']
