from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    redis_host: str = Field('http://127.0.0.1', env='REDIS_HOST')


test_settings = TestSettings()
