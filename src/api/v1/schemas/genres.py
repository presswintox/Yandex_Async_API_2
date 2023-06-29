from typing import Optional
from pydantic import Field
from src.api.v1.schemas.base import BaseUUIDMixin, PaginationMixin


class GenreListDetail(BaseUUIDMixin):
    """Модель для списка жанров"""
    title: str = Field(..., alias='name')


class GenreDetail(BaseUUIDMixin):
    """Модель для детальной информации о жанре"""
    title: str = Field(..., alias='name')
    description: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


class GenreSearchQuery(
            PaginationMixin,
        ):
    """Query-параметры для поиска жанров

    query: str - поисковый запрос
    """
    query: str = ''


class GenreListQuery(PaginationMixin):
    """Query-параметры для списка жанров
    """
