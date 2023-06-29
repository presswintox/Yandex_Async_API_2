from typing import List
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, validator

from src.api.v1.schemas.base import PaginationMixin, BaseUUIDMixin


class FilmListDetail(BaseUUIDMixin):
    """Модель для списка фильмов"""
    title: str
    imdb_rating: float


class GenreDetail(BaseUUIDMixin):
    """Модель для жанра"""
    name: str

    class Config:
        allow_population_by_field_name = True


class PersonDetail(BaseUUIDMixin):
    """Модель для персоны"""
    full_name: str

    class Config:
        allow_population_by_field_name = True


class FilmDetail(BaseUUIDMixin):
    """Модель для детальной информации о фильме"""
    title: str
    imdb_rating: float
    description: str
    genre: List[GenreDetail] = []
    actors: List[PersonDetail] = []
    writers: List[PersonDetail] = []
    directors: List[PersonDetail] = []

    class Config:
        allow_population_by_field_name = True


class FilmSortMixin(BaseModel):
    """Миксин для сортировки фильмов"""
    sort: str = '-imdb_rating'

    @validator("sort", always=True)
    def validate_sort(cls, value, values):
        valid_fields = ['imdb_rating']
        if len(value) > 1:
            if value[0] == '-':
                field = value[1:]
                value = field + ':desc'
            else:
                field = value
                value = field + ':asc'

            if field not in valid_fields:
                raise HTTPException(status_code=400,
                                    detail='Invalid sort field')
            return value
        raise HTTPException(status_code=400, detail='Invalid sort field')


class FilmSearchQuery(PaginationMixin, FilmSortMixin):
    """Query-параметры для поиска фильмов

    query: str - поисковый запрос
    """
    query: str = ''


class FilmListQuery(PaginationMixin, FilmSortMixin):
    """Query-параметры для списка фильмов

    genre: UUID - фильтр по жанру
    """
    genre: UUID = None
