import time

from elasticsearch import Elasticsearch

from tests.functional.settings import TestSettings

if __name__ == '__main__':
    es_client = Elasticsearch(hosts=TestSettings.es_host,
                              verify_certs=False)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
