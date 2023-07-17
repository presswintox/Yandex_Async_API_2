from functools import lru_cache
from typing import List

from elasticsearch import NotFoundError
from fastapi import Depends

from src.db.abstract import AsyncCacheStorage, AsyncSearchStorage
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.genre import Genre
from src.services.base import BaseService


class GenreService(BaseService):
    """Сервис для работы с жанрами

    elastic - подключение к Elasticsearch
    """
    index = "genres"
    model = Genre

    async def search_by_filter(
                                self,
                                page_size: int,
                                page_number: int,
                                search: str = ''
                               ) -> List[Genre]:
        """Поиск жанра по фильтру"""
        query = f"{page_size}_{page_number}_{search}"
        genres = await self._get_objects_from_cache(query)
        if not genres:
            genres = await self._search_genres_from_es(page_size,
                                                       page_number, search)
            if genres is None:
                return []

            await self._put_objects_to_cache_by_query(query, genres)
        if genres is None:
            return []
        return genres

    async def _search_genres_from_es(self, page_size: int, page_number: int,
                                     search: str = '') -> List[Genre]:
        """Поиск жанров по фильтру в Elasticsearch

        :param page_size: количество жанров на странице
        :param page_number: номер страницы
        :param search: поисковый запрос
        """
        result = []
        matches = dict()

        if search != '':
            matches['query'] = search
            matches['fields'] = [
                "name",
                "description",
            ]

        if len(matches) == 0:
            query = {"match_all": {}}
        else:
            query = {"multi_match": matches}

        _from = page_size * (page_number - 1)
        try:
            genres = await self.storage.search(
                                                index="genres",
                                                from_=_from,
                                                size=page_size,
                                                query=query
                                              )
        except NotFoundError:
            return []

        for genre in genres.body['hits']['hits']:
            result.append(Genre(**genre["_source"]))
        return result


@lru_cache()
def get_genre_service(storage: AsyncSearchStorage = Depends(get_elastic),
                      cache: AsyncCacheStorage = Depends(get_redis)) \
        -> GenreService:
    """Получение сервиса для работы с жанрами"""
    return GenreService(storage, cache)
