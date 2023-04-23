from abc import ABC, abstractmethod

from aio_pika import IncomingMessage


class Message(ABC):
    @abstractmethod
    async def handle(self, message: IncomingMessage):
        pass
