import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio.client import Redis
from src.db import redis
from src.api.v1 import films, genres, persons
from src.core.config import settings
from src.db import elastic
from src.db.elastic import ElasticStorage
from src.db.redis import RedisStorage

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='API для работы с фильмами, жанрами и участниками. '
                'Используется полнотекстовый поиск из ElasticSearch.',

)


@app.on_event('startup')
async def startup():
    host = f'http://{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'
    redis.redis = RedisStorage(Redis(host=settings.REDIS_HOST,
                                     port=settings.REDIS_PORT),
                               settings.FILM_CACHE_EXPIRE_IN_SECONDS)
    elastic.es = ElasticStorage(AsyncElasticsearch(hosts=[host]))


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['Фильмы'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['Жанры'])
app.include_router(persons.router, prefix='/api/v1/persons',
                   tags=['Участники'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='localhost',
        port=8000,
    )
