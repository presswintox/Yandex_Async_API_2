import enum
from typing import List, Optional

from src.models.base import BaseMixin


class Person(BaseMixin):
    full_name: str


class Actor(Person):
    pass


class Director(Person):
    pass


class Writer(Person):
    pass


class PersonWithFilms(Person):
    pass


class RoleEnum(enum.Enum):
    DIRECTOR = 'director'
    ACTOR = 'actor'
    WRITER = 'writer'


class FilmWithPersonRoles(BaseMixin):
    roles: List[str]


class PersonDetail(BaseMixin):
    full_name: str
    films: Optional[List[FilmWithPersonRoles]]
