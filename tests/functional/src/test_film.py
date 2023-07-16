import pytest

from elasticbuild.pyfiles.moviessettings import ES_SCHEMA
from tests.functional.testdata.init_data import FILMS_DATA
from tests.functional.settings import test_settings

URL_SEARCH = test_settings.service_url + '/api/v1/films/'
INDEX = 'movies'
FIRST_FILM_ID = FILMS_DATA[0]['id']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {},
            {'status': 200, 'length': 10}
        ),
        (
                {'page_size': 5, 'page_number': 1},
                {'status': 200, 'length': 5}
        ),
        (
                {'page_size': 5, 'page_number': 1, 'sort': '123123'},
                {'status': 400, 'length': 1}
        ),
        (
                {'genre': '97f168bd-d10d-481b-ad38-89d252a13feb'},
                {'status': 200, 'length': 10}
        )
    ]
)
@pytest.mark.asyncio
async def test_films(es_write_data,
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
            {},
            {'status': 200, 'length': 10}
        ),
        (
            {'page_size': 5, 'page_number': 1},
            {'status': 200, 'length': 5}
        ),
        (
                {'page_size': 5, 'page_number': 1, 'sort': '123123'},
                {'status': 400, 'length': 1}
        ),
        (
                {'genre': '97f168bd-d10d-481b-ad38-89d252a13feb'},
                {'status': 200, 'length': 10}
        )
    ]
)
@pytest.mark.asyncio
async def test_films_with_redis(redis_write_data,
                                make_get_request,
                                query_data: dict,
                                expected_answer: dict):
    await redis_write_data(INDEX, query_data,  FILMS_DATA)
    response, status = await make_get_request(url=URL_SEARCH,
                                              params=query_data)

    assert status == expected_answer['status']
    assert len(response) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': FIRST_FILM_ID},
                {'status': 200}
        )
    ]
)
@pytest.mark.asyncio
async def test_film_by_id(es_write_data,
                          make_get_request,
                          elas_init_index,
                          query_data: dict,
                          expected_answer: dict):
    await elas_init_index(INDEX, ES_SCHEMA)
    await es_write_data(INDEX, FILMS_DATA)
    response, status = await make_get_request(url=URL_SEARCH+query_data['id'],
                                              params=query_data)

    assert status == expected_answer['status']
