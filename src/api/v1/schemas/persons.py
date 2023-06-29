from typing import List, Optional

from src.api.v1.schemas.base import PaginationMixin, BaseUUIDMixin


class FilmWithPersonRoles(BaseUUIDMixin):
    roles: List[str]


class PersonDetail(BaseUUIDMixin):
    full_name: str
    films: Optional[List[FilmWithPersonRoles]]


class PersonSearchQuery(PaginationMixin):
    """
    Query-параметры для поиска персон

    query: str - поисковый запрос
    """
    query: str = ""
