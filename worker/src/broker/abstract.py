from abc import ABC, abstractmethod


class Broker(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def create_channel(self):
        pass

    @abstractmethod
    async def get_queue(self, queue_name):
        pass

    @abstractmethod
    async def consume(self, queue, callback):
        pass
