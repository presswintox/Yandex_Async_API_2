import logging
import backoff
from dotenv import load_dotenv
import elastic_transport
from elasticsearch import helpers
from personssettings import ESP_SCHEMA
from genressettings import ESG_SCHEMA
from moviessettings import ES_SCHEMA
from envload import Env
import json
from managers import elas_context

load_dotenv()


def bo_timegen() -> float:
    times = [1.0, 2.0, 5.0]
    for t in times:
        yield t
    while True:
        yield 10.0


@backoff.on_exception(
    wait_gen=bo_timegen,
    exception=elastic_transport.ConnectionError,
    jitter=None,)
def elas_init(env: dict, index: str, body: str):
    """
    Запись схемы данных ElasticSearch
    (обёрнут в backoff)

    Args:
        env (Env): dict[host: str, port: int]
    """
    logging.info(f'(backoff) Установка схемы эластика ({index})')
    with elas_context(env) as elas_conn:
        if not elas_conn.indices.exists(index=index):
            elas_conn.indices.create(
                index=index,
                ignore=400,
                body=body
            )


@backoff.on_exception(
    wait_gen=bo_timegen,
    exception=elastic_transport.ConnectionError,
    jitter=None,)
def fill_data(env: dict, index: str):
    """
    Заполняет данными еластик из подготовленного файла JSON

    Args:
        env (Env): dict[host: str, port: int]
        index (str): наименование заполняемого индакса в эластике
    """
    logging.info(f'(backoff) Заполнение {index}')
    with elas_context(env) as elascon:
        with open(f"{index}.json") as f:
            jeyson = json.load(f)
        helpers.bulk(
            client=elascon,
            index=index,
            actions=jeyson,
            raise_on_error=True,
        )


if __name__ == '__main__':

    env = Env()

    logfile: str = 'setupelastic.log'
    with open(logfile, 'w'):
        pass

    logging.basicConfig(
        filename=logfile,
        format='%(asctime)s - %(message)s',
        level=logging.INFO,
        encoding='utf-8',
    )
    logging.info('---<( начало )>---')

    elas_init(env.dict(), index='movies', body=ES_SCHEMA)
    fill_data(env=env.dict(), index='movies')
    elas_init(env.dict(), index='genres', body=ESG_SCHEMA)
    fill_data(env=env.dict(), index='genres')
    elas_init(env.dict(), index='persons', body=ESP_SCHEMA)
    fill_data(env=env.dict(), index='persons')
    logging.info('---<( конец )>---')
