from typing import Optional

from elasticsearch import AsyncElasticsearch


es: Optional[AsyncElasticsearch] = None


async def get_elastic() -> AsyncElasticsearch:
    """Получение подключения к Elasticsearch"""
    return es
