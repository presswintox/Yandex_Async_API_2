import json
from typing import Optional, List, Type

from elasticsearch import NotFoundError
from pydantic import parse_raw_as
from pydantic.json import pydantic_encoder

from src.db.elastic import ElasticStorage
from src.db.redis import RedisStorage
from src.models.base import BaseMixin
from src.models.film import Film


class BaseService:
    """Базовый сервис для работы с Elasticsearch и Redis
    По умолчанию используется модель Film

    elastic - подключение к Elasticsearch
    redis - подключение к Redis
    index - индекс Elasticsearch
    model - модель данных
    """
    index: str = 'movies'
    model = Film

    def __init__(self, elastic, redis):
        self.elastic: ElasticStorage = elastic
        self.redis: RedisStorage = redis

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
        """Получение объекта по id из Elasticsearch

        :param _id: id объекта
        """
        try:
            object = await self.elastic.get(index=self.index, identifier=_id)
        except NotFoundError:
            return None
        return self.model(**object.body["_source"])

    async def _object_from_cache(self, _id: str,
                                 parse_model: Type[BaseMixin] = None,
                                 index_name: str = None) \
            -> Optional[BaseMixin]:
        """Получение объекта из кеша Redis

           :param _id: id объекта
           :return: объект модели
        """
        if index_name is None:
            index_name = self.index
        data = await self.redis.get(index_name, _id)
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
        """Получение объектов по query из кеша Redis

           :param query: поисковый запрос
           :return: cписок объектов фильмов
        """
        if index_name is None:
            index_name = self.index
        data = await self.redis.get(index_name, query)
        if not data:
            return None
        if parse_model:
            return parse_raw_as(List[parse_model], data)
        return parse_raw_as(List[self.model], data)

    async def _put_object_to_cache(self, obj: BaseMixin,
                                   index_name: str = None):
        """Сохранение объекта в кеш Redis

        :param obj: объект
        """
        if index_name is None:
            index_name = self.index
        await self.redis.set(index=index_name,
                             obj=obj.json(),
                             identifier=str(obj.id))

    async def _put_objects_to_cache_by_query(self, query: str,
                                             objs: List[BaseMixin],
                                             index_name: str = None):
        """Сохранение объектов по query в кеш Redis

        :param query: поисковый запрос
        :param objs: объект
        """
        if index_name is None:
            index_name = self.index
        redis_data = json.dumps(objs, default=pydantic_encoder)
        await self.redis.set(index=index_name,
                             obj=redis_data,
                             identifier=query)
