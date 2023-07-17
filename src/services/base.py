import json
from typing import Optional, List, Type

from elasticsearch import NotFoundError
from pydantic import parse_raw_as
from pydantic.json import pydantic_encoder

from src.db.abstract import AsyncCacheStorage, AsyncSearchStorage
from src.models.base import BaseMixin
from src.models.film import Film


class BaseService:
    """Базовый сервис для работы с хранителями данных и кешом
    По умолчанию используется модель Film

    storage - подключение к storage данных
    cache - подключение к хранителю кэша
    index - индекс в storage
    model - модель данных
    """
    index: str = 'movies'
    model = Film

    def __init__(self, storage, cache):
        self.storage: AsyncSearchStorage = storage
        self.cache: AsyncCacheStorage = cache

    async def get_by_id(self, _id: str) -> Optional[BaseMixin]:
        """Получение объекта по id

        :param _id: id объекта
        """

        object = await self._object_from_cache(_id)
        if not object:
            object = await self._get_object_from_es(_id)
            if object is None:
                return None
            await self._put_object_to_cache(object)
        return object

    async def _get_object_from_es(self, _id: str) -> Optional[BaseMixin]:
        """Получение объекта по id из Storage

        :param _id: id объекта
        """
        try:
            object = await self.storage.get(index=self.index, identifier=_id)
        except NotFoundError:
            return None
        return self.model(**object.body["_source"])

    async def _object_from_cache(self, _id: str,
                                 parse_model: Type[BaseMixin] = None,
                                 index_name: str = None) \
            -> Optional[BaseMixin]:
        """Получение объекта из кеша

           :param _id: id объекта
           :return: объект модели
        """
        if index_name is None:
            index_name = self.index
        data = await self.cache.get(index_name, _id)
        if not data:
            return None
        if parse_model:
            return parse_model.parse_raw(data)
        return self.model.parse_raw(data)

    async def _get_objects_from_cache(self,
                                      query: str,
                                      parse_model: Type[BaseMixin] = None,
                                      index_name: str = None) \
            -> Optional[List[BaseMixin]]:
        """Получение объектов по query из кеша

           :param query: поисковый запрос
           :return: cписок объектов фильмов
        """
        if index_name is None:
            index_name = self.index
        data = await self.cache.get(index_name, query)
        if not data:
            return None
        if parse_model:
            return parse_raw_as(List[parse_model], data)
        return parse_raw_as(List[self.model], data)

    async def _put_object_to_cache(self, obj: BaseMixin,
                                   index_name: str = None):
        """Сохранение объекта в кеш

        :param obj: объект
        """
        if index_name is None:
            index_name = self.index
        await self.cache.set(index=index_name,
                             obj=obj.json(),
                             identifier=str(obj.id))

    async def _put_objects_to_cache_by_query(self, query: str,
                                             objs: List[BaseMixin],
                                             index_name: str = None):
        """Сохранение объектов по query в кеш

        :param query: поисковый запрос
        :param objs: объект
        """
        if index_name is None:
            index_name = self.index
        cache_data = json.dumps(objs, default=pydantic_encoder)
        await self.cache.set(index=index_name,
                             obj=cache_data,
                             identifier=query)
