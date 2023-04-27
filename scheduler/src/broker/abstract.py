from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel


class Broker(ABC):
    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def consume(self, queue, callback):
        pass

    @abstractmethod
    async def publish(self, exchange_name: str, msg: Type[BaseModel], routing_key: str):
        pass
