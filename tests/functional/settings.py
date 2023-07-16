from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('localhost', env='ELASTIC_HOST')
    es_port: int = Field(9200, env='ELASTIC_PORT')
    redis_host: str = Field('localhost', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
    service_url: str = Field('http://localhost:8000', env='SERVICE_URL')


test_settings = TestSettings()
