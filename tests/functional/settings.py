from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://elastic:9200', env='ELASTIC_HOST')
    redis_host: str = Field('redis', env='REDIS_HOST')

    es_index: str = 'movies'
    es_id_field: str = 'id'
    service_url: str = 'http://backend:8000'


test_settings = TestSettings()
