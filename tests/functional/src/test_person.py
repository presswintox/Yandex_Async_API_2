from http import HTTPStatus

import pytest

from elasticbuild.pyfiles.moviessettings import ES_SCHEMA
from elasticbuild.pyfiles.personssettings import ESP_SCHEMA
from tests.functional.testdata.init_data import PERSONS_DATA, FILMS_DATA
from tests.functional.settings import test_settings

URL_PERSON = test_settings.service_url + '/api/v1/persons/'
INDEX = 'persons'

FIRST_PERSON_ID = PERSONS_DATA[0]['id']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {},
                {'status': HTTPStatus.OK, 'length': 10}
        ),
        (
                {'query': 'Ann', 'page_size': 5, 'page_number': 1},
                {'status': HTTPStatus.OK, 'length': 5}
        ),
        (
                {'page_size': 20, 'page_number': 1},
                {'status': HTTPStatus.OK, 'length': 10}
        ),
        (
                {'page_size': 10, 'page_number': 2},
                {'status': HTTPStatus.OK, 'length': 10}
        ),
        (
                {'query': 'Not exist person'},
                {'status': HTTPStatus.OK, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_persons(es_write_data,
                       make_get_request,
                       elas_init_index,
                       query_data: dict,
                       expected_answer: dict):
    await elas_init_index(INDEX, ESP_SCHEMA)
    await es_write_data(INDEX, PERSONS_DATA)
    response, status = await make_get_request(url=URL_PERSON + 'search',
                                              params=query_data)

    assert status == expected_answer['status']
    assert len(response) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {},
            {'status': HTTPStatus.OK, 'length': 10}
        ),
        (
                {'query': 'Ann', 'page_size': 5, 'page_number': 1},
                {'status': HTTPStatus.OK, 'length': 5}
        ),
        (
                {'page_size': 20, 'page_number': 1},
                {'status': HTTPStatus.OK, 'length': 10}
        ),
        (
                {'page_size': 10, 'page_number': 2},
                {'status': HTTPStatus.OK, 'length': 10}
        ),
        (
                {'query': 'Not exist person'},
                {'status': HTTPStatus.OK, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_persons_with_redis(redis_write_data,
                                  make_get_request,
                                  query_data: dict,
                                  expected_answer: dict):
    await redis_write_data(INDEX, query_data,
                           PERSONS_DATA)
    response, status = await make_get_request(url=URL_PERSON + 'search',
                                              params=query_data)

    assert status == expected_answer['status']
    assert len(response) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': FIRST_PERSON_ID},
                {'status': HTTPStatus.OK}
        )
    ]
)
@pytest.mark.asyncio
async def test_person_by_id(es_write_data,
                            make_get_request,
                            elas_init_index,
                            query_data: dict,
                            expected_answer: dict):
    await elas_init_index(INDEX, ESP_SCHEMA)
    await es_write_data(INDEX, PERSONS_DATA)
    response, status = await make_get_request(
        url=URL_PERSON + query_data['id'])

    assert status == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': FIRST_PERSON_ID},
                {'status': HTTPStatus.OK, 'length': 10}
        )
    ]
)
@pytest.mark.asyncio
async def test_person_films_by_id(es_write_data,
                                  make_get_request,
                                  elas_init_index,
                                  query_data: dict,
                                  expected_answer: dict):

    await elas_init_index(INDEX, ESP_SCHEMA)
    await es_write_data(INDEX, PERSONS_DATA)

    await elas_init_index('movies', ES_SCHEMA)
    await es_write_data('movies', FILMS_DATA)

    response, status = await make_get_request(
        url=URL_PERSON + query_data['id'] + '/film')

    assert status == expected_answer['status']
    assert len(response) == expected_answer['length']
