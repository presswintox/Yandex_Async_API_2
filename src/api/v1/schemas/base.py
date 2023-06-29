from pydantic import BaseModel, validator, Field
from uuid import UUID


class PaginationMixin(BaseModel):
    """Query параметры для пагинации

    page_size - максимальное значение 1000, минимальное значение 1
    page_number - минимальное значение 1
    """
    page_size: int = 50
    page_number: int = 1

    @validator("page_size", always=True)
    def validate_page_size(cls, value, values):
        if value > 1000 or value < 1:
            return 50
        return value

    @validator("page_number", always=True)
    def validate_page_number(cls, value, values):
        if value < 1:
            return 1
        return value


class BaseUUIDMixin(BaseModel):
    """Базовый класс для моделей с UUID в качестве идентификатора"""
    id: UUID = Field(..., alias='uuid')

    class Config:
        allow_population_by_field_name = True
