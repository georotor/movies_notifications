from abc import ABC, abstractmethod
from typing import Any, Callable


class Broker(ABC):
    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def consume(self, queue_name: str, callback: Callable[[dict], Any]):
        pass
