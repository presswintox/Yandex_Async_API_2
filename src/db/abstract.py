from abc import ABC, abstractmethod


class BaseStorageInterface(ABC):

    @abstractmethod
    async def get(self, index: str, identifier: str = None):
        pass

    @abstractmethod
    async def close(self):
        pass


class SearchStorageInterface(ABC):

    @abstractmethod
    async def search(self, **kwargs):
        pass


class SetStorageInterface(ABC):

    @abstractmethod
    def set(self, index: str, obj: str, identifier: str = None, **kwargs):
        pass
