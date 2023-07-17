import uuid
from functools import lru_cache
from typing import List

from elasticsearch import NotFoundError
from fastapi import Depends

from src.db.abstract import AsyncCacheStorage, AsyncSearchStorage
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import Film
from src.services.base import BaseService


class FilmService(BaseService):

    index: str = 'movies'
    model = Film

    """Сервис для работы с фильмами"""

    async def search_by_filter(self,
                               sort: str,
                               page_size: int,
                               page_number: int,
                               genre: uuid.UUID | None = None,
                               search: str = ''
                               ) -> List[Film]:
        """Поиск фильмов по фильтру"""
        sort_redis = sort.replace(':', '_')

        if genre is not None:
            query = f"{sort_redis}_{page_size}_{page_number}_{str(genre)}_{search}"
        else:
            query = f"{sort_redis}_{page_size}_{page_number}_{search}"

        films = await self._get_objects_from_cache(query)
        if not films:
            films = await self._search_films_from_es(sort, page_size,
                                                     page_number, genre, search)
            if films is None:
                return []
            await self._put_objects_to_cache_by_query(query, films)

        return films

    async def _search_films_from_es(self, sort: str,
                                    page_size: int,
                                    page_number: int,
                                    genre: uuid.UUID | None = None,
                                    search: str = '') -> List[Film]:
        """Поиск фильмов по фильтру в Elasticsearch

        :param sort: сортировка
        :param page_size: количество фильмов на странице
        :param page_number: номер страницы
        :param genre: жанр фильма
        :param search: поисковый запрос
        """
        result = []
        matches = dict()

        if genre is not None:
            matches["nested"] = {
                    "path": "genre",
                    "query": {
                        "bool": {
                            "must": [
                                {"match": {"genre.id": genre}}
                            ]
                        }
                    }
            }
        if search != '':
            matches["multi_match"] = {
                "query": search,
                "fields": ["title", "description"]
            }
        if len(matches) == 0:
            query = {"match_all": {}}
        else:
            query = matches

        _from = page_size * (page_number - 1)
        try:
            films = await self.storage.search(index="movies",
                                              sort=sort,
                                              from_=_from,
                                              size=page_size,
                                              query=query
                                              )
        except NotFoundError:
            return []

        for film in films.body['hits']['hits']:
            result.append(Film(**film["_source"]))
        return result


@lru_cache()
def get_film_service(cache: AsyncCacheStorage = Depends(get_redis),
                     storage: AsyncSearchStorage = Depends(get_elastic)
                     ) -> FilmService:
    """Получение сервиса для работы с фильмами"""
    return FilmService(storage, cache)
