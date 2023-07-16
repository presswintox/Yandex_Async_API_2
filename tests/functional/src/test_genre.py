import pytest

from elasticbuild.pyfiles.genressettings import ESG_SCHEMA
from tests.functional.testdata.init_data import GENRE_DATA
from tests.functional.settings import test_settings

URL_GENRE = test_settings.service_url + '/api/v1/genres/'
INDEX = 'genres'
FIRST_GENRE_ID = GENRE_DATA[0]['id']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {},
            {'status': 200, 'length': 10}
        ),
        (
                {'query': 'Sci', 'page_size': 5, 'page_number': 1},
                {'status': 200, 'length': 5}
        ),
        (
                {'page_size': 20, 'page_number': 1},
                {'status': 200, 'length': 10}
        ),
        (
                {'page_size': 10, 'page_number': 2},
                {'status': 200, 'length': 10}
        ),
        (
                {'query': 'Not exist genre'},
                {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_genres_by_search(es_write_data,
                                make_get_request,
                                elas_init_index,
                                query_data: dict,
                                expected_answer: dict):
    await elas_init_index(INDEX, ESG_SCHEMA)
    await es_write_data(INDEX, GENRE_DATA)
    response, status = await make_get_request(url=URL_GENRE + 'search',
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
                {'page_size': 20, 'page_number': 1},
                {'status': 200, 'length': 10}
        ),
        (
                {'page_size': 10, 'page_number': 2},
                {'status': 200, 'length': 10}
        )
    ]
)
@pytest.mark.asyncio
async def test_genres(es_write_data,
                      make_get_request,
                      elas_init_index,
                      query_data: dict,
                      expected_answer: dict):
    await elas_init_index(INDEX, ESG_SCHEMA)
    await es_write_data(INDEX, GENRE_DATA)
    response, status = await make_get_request(url=URL_GENRE,
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
                {'query': 'Sci', 'page_size': 5, 'page_number': 1},
                {'status': 200, 'length': 5}
        ),
        (
                {'page_size': 20, 'page_number': 1},
                {'status': 200, 'length': 10}
        ),
        (
                {'page_size': 10, 'page_number': 2},
                {'status': 200, 'length': 10}
        ),
        (
                {'query': 'Not exist genre'},
                {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_genres_with_redis(redis_write_data,
                                 make_get_request,
                                 query_data: dict,
                                 expected_answer: dict):
    await redis_write_data(INDEX, query_data,
                           GENRE_DATA)
    response, status = await make_get_request(url=URL_GENRE + 'search',
                                              params=query_data)

    assert status == expected_answer['status']
    assert len(response) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': FIRST_GENRE_ID},
                {'status': 200}
        )
    ]
)
@pytest.mark.asyncio
async def test_genre_by_id(es_write_data,
                           make_get_request,
                           elas_init_index,
                           query_data: dict,
                           expected_answer: dict):
    await elas_init_index(INDEX, ESG_SCHEMA)
    await es_write_data(INDEX, GENRE_DATA)
    response, status = await make_get_request(
        url=URL_GENRE + query_data['id'])

    assert status == expected_answer['status']
