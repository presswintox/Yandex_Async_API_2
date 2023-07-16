from typing import Optional

from elasticsearch import AsyncElasticsearch

from .abstract import BaseStorageInterface, SearchStorageInterface


class ElasticStorage(BaseStorageInterface, SearchStorageInterface):
    def __init__(self, session: AsyncElasticsearch):
        self.session = session

    async def get(self, index: str, identifier: str = None):
        return await self.session.get(index=index, id=identifier)

    async def search(self, **kwargs):
        return await self.session.search(
            index=kwargs.get("index"),
            from_=kwargs.get('_from'),
            size=kwargs.get('size'),
            query=kwargs.get('query'),
        )

    async def close(self):
        await self.session.close()


es: Optional[ElasticStorage] = None


async def get_elastic() -> ElasticStorage:
    """Получение подключения к Elasticsearch"""
    return es
