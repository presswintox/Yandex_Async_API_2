import uuid

from orjson import orjson

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseMixin(BaseModel):
    id: uuid.UUID

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
