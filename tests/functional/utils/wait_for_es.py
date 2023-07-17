import backoff
from elasticsearch import Elasticsearch, ConnectionError, ConnectionTimeout


@backoff.on_exception(
    backoff.expo, (ConnectionError, ConnectionTimeout)
)
def waiter():
    print('Waiting for ElasticSearch')
    es_client = Elasticsearch(hosts=['http://elastic:9200'],
                              verify_certs=False)

    if not es_client.ping():
        print('ElasticSearch is not available')
        raise ConnectionError('ElasticSearch is not available')


if __name__ == '__main__':
    waiter()
