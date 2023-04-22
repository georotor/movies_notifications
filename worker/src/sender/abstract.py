from abc import ABC, abstractmethod


class Sender(ABC):
    @abstractmethod
    async def send(self, to, subject, body):
        pass
