from typing import Optional

from elasticsearch import AsyncElasticsearch

from .abstract import StorageInterface


class ElasticStorage(StorageInterface):
    def __init__(self, session: AsyncElasticsearch):
        self.session = session

    async def get(self, index: str, identifier: str = None):
        return await self.session.get(index=index, id=identifier)

    async def search(self, **kwargs):
        return await self.session.search(
            index=kwargs.get("index"),
            from_=kwargs.get('_from'),
            size=kwargs.get('page_size'),
            query=kwargs.get('query'),
        )

    async def close(self):
        await self.session.close()


es: Optional[ElasticStorage] = None


async def get_elastic() -> StorageInterface:
    """Получение подключения к Elasticsearch"""
    return es
