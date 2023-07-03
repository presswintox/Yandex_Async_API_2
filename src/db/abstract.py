from abc import ABC, abstractmethod


class StorageInterface(ABC):
    @abstractmethod
    async def get(self, index: str, identifier: str = None):
        pass

    @abstractmethod
    async def search(self, **kwargs):
        pass

    @abstractmethod
    async def close(self):
        pass


class DownloadStorageInterface(ABC):

    @abstractmethod
    def put(self, index: str, identifier: str = None):
        pass
