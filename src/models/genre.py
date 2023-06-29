from typing import Optional
from src.models.base import BaseMixin


class Genre(BaseMixin):
    name: str
    description: Optional[str] = None
