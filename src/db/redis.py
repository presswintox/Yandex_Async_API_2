from typing import Optional
from redis.asyncio import Redis

from src.db.abstract import BaseStorageInterface, SetStorageInterface


class RedisStorage(BaseStorageInterface, SetStorageInterface):
    def __init__(self, session: Redis, expire_in_seconds: int = None):
        self.expire_in_seconds = expire_in_seconds
        self.session = session

    async def get(self, index: str, identifier: str = None):
        return await self.session.get(f'{index}:{identifier}')

    async def close(self):
        await self.session.close()

    async def set(self, index: str, obj: str, identifier: str = None,
                  **kwargs):
        expire_in_seconds = kwargs.get('expire_in_seconds') \
                            or self.expire_in_seconds
        await self.session.set(f'{index}:{identifier}', obj, expire_in_seconds)


redis: Optional[RedisStorage] = None


async def get_redis() -> RedisStorage:
    return redis
