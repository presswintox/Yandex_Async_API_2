import uuid
from functools import lru_cache
from typing import List

from elasticsearch import NotFoundError
from fastapi import Depends

from src.db.abstract import AsyncCacheStorage, AsyncSearchStorage
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import Film
from src.models.person import Person, RoleEnum, FilmWithPersonRoles, \
    PersonDetail
from src.services.base import BaseService


class PersonService(BaseService):
    index = "persons"
    model = Person

    async def get_persons_with_films_by_query(self, page_size: int,
                                              page_number: int,
                                              search: str = "") \
            -> List[PersonDetail]:
        """Поиск фильмов по фильтру"""
        query = f"{page_size}_{page_number}_{search}"

        person_detail_list = await self._get_objects_from_cache(query,
                                                                PersonDetail)
        if not person_detail_list:

            person_list = await self.search_by_filter(
                page_size=page_size,
                page_number=page_number,
                search=search
            )
            person_detail_list = (
                await self.get_persons_with_films_and_roles(person_list)
            )
            if person_detail_list is None:
                return []
            await self._put_objects_to_cache_by_query(query, person_detail_list)

        return person_detail_list

    async def search_by_filter(
        self,
        page_size: int,
        page_number: int,
        search: str = "",
    ) -> List[Person]:
        """Поиск фильмов по фильтру

        :param page_size: количество фильмов на странице
        :param page_number: номер страницы
        :param search: поисковый запрос
        """

        persons = await self._search_persons_from_es(
            page_size=page_size,
            page_number=page_number,
            search=search,
        )

        if persons is None:
            return []

        return persons

    async def search_films_by_person_uid(
        self, person_id: uuid.UUID
    ) -> List[Film]:
        """
        Поиск фильмов по персоне

        :param person_id: id персоны
        """

        films = await self._get_objects_from_cache(str(person_id), Film,
                                                   "person_films")
        if not films:
            person_id_list = [person_id]

            if isinstance(person_id, list):
                person_id_list = person_id

            films = await self.search_films_by_person_uid_list(
                person_id_list=person_id_list
            )
            if films is None:
                return []

            await self._put_objects_to_cache_by_query(str(person_id), films,
                                                      "person_films")

        return films

    async def search_films_by_person_uid_list(
        self, person_id_list: List[uuid.UUID]
    ) -> List[Film]:
        """
        Получение фильмов по списку персон

        :param person_id_list: скисок id персон
        """
        query = {
            "bool": {
                "should": [
                    {
                        "nested": {
                            "path": f"{role.value}s",
                            "query": {
                                "terms": {
                                    f"{role.value}s.id": person_id_list
                                }
                            }
                        }
                    }
                    for role in RoleEnum
                ],
            },
        }

        films = await self.storage.search(
            index="movies",
            query=query,
        )

        films_obj_list = [
            Film(**film["_source"]) for film in films.body["hits"]["hits"]
        ]

        return films_obj_list

    async def get_person_films_with_roles(
        self, person_id: uuid.UUID, film_list: List[Film]
    ) -> List[FilmWithPersonRoles]:
        """
        Получение персон с фильмами и ролями в них

        :param person_id: id персоны
        :param film_list: список фильмов
        """
        matched_data = []
        for film in film_list:
            roles = []
            if person_id in [person.id for person in film.directors]:
                roles.append(RoleEnum.DIRECTOR.value)
            if person_id in [person.id for person in film.actors]:
                roles.append(RoleEnum.ACTOR.value)
            if person_id in [person.id for person in film.writers]:
                roles.append(RoleEnum.WRITER.value)

            if roles:
                film_short = FilmWithPersonRoles(id=film.id, roles=set(roles))
                matched_data.append(film_short)
        return matched_data

    async def get_person_with_films_and_roles(
        self, person_id: uuid.UUID
    ) -> PersonDetail | None:
        """
        Получение данных по персоне со списком фильмов и ролями в них

        :param person_id: id персоны
        """

        person_detail = await self._object_from_cache(str(person_id),
                                                      PersonDetail,
                                                      "person_detail")

        if not person_detail:

            person = await self._get_object_from_es(str(person_id))
            if person is None:
                return None

            films = await self.search_films_by_person_uid(person_id=person.id)
            films_and_roles = await self.get_person_films_with_roles(
                person_id=person.id, film_list=films
            )
            person_detail = PersonDetail(
                films=films_and_roles, **person.dict()
            )
            await self._put_object_to_cache(person_detail, "person_detail")

        return person_detail

    async def get_persons_with_films_and_roles(
        self, person_list: List[Person]
    ) -> List[PersonDetail]:
        """
        Получение данных по персоне со списком фильмов и ролями в них

        :param person_list: скисок персон
        """
        person_id_list = [person.id for person in person_list]

        films = await self.search_films_by_person_uid_list(
            person_id_list=person_id_list
        )

        person_detail_list = []
        for person in person_list:
            films_and_roles = await self.get_person_films_with_roles(
                person_id=person.id, film_list=films
            )
            person_detail = PersonDetail(
                films=films_and_roles, **person.dict()
            )
            person_detail_list.append(person_detail)

        return person_detail_list

    async def _search_persons_from_es(
        self,
        page_size: int,
        page_number: int,
        search: str = ""
    ) -> List[Person]:
        """Поиск персоны по фильтру в Elasticsearch

        :param page_size: количество фильмов на странице
        :param page_number: номер страницы
        :param search: поисковый запрос
        """
        result = []
        matches = dict()

        if search != "":
            matches["full_name"] = {
                "query": search,
                "operator": "and"
            }

        if len(matches) == 0:
            query = {"match_all": {}}
        else:
            query = {"match": matches}

        _from = page_size * (page_number - 1)
        try:
            persons = await self.storage.search(
                index="persons",
                from_=_from,
                size=page_size,
                query=query,
            )
        except NotFoundError:
            return []

        for person in persons.body["hits"]["hits"]:
            result.append(Person(**person["_source"]))
        return result


@lru_cache()
def get_person_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        storage: AsyncSearchStorage = Depends(get_elastic),
) -> PersonService:
    return PersonService(storage, cache)
