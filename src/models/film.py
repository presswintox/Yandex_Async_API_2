from typing import List, Optional

from src.models.base import BaseMixin
from src.models.genre import Genre
from src.models.person import Actor, Writer, Director


class Film(BaseMixin):
    title: str
    description: str
    imdb_rating: float
    genre: List[Genre]
    actors: List[Actor]
    writers: List[Writer]
    directors: Optional[List[Director]] = []
    actors_names: Optional[List[str]] = []
    writers_names: Optional[List[str]] = []
