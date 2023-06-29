from elasticsearch import Elasticsearch
from contextlib import contextmanager


@contextmanager
def elas_context(env: dict):
    """
    Соединение с ElasticSearch

    Args:
        env (dict): Параметры приложения

    Returns:
        Elasticsearch: Экземпляр соединения
    """
    conn = Elasticsearch('http://{h}:{p}'.format(h=env['host'], p=env['port']))
    try:
        yield conn
    finally:
        conn.close()
