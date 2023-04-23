from abc import ABC, abstractmethod


class SenderError(Exception):
    """Базовое исключение для ошибок."""


class Sender(ABC):
    @abstractmethod
    async def send(self, to, subject, body):
        pass
