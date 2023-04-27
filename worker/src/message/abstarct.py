from abc import ABC, abstractmethod


class Message(ABC):
    @abstractmethod
    async def handle(self, context: dict):
        pass
