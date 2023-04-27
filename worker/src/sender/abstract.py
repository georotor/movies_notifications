from abc import ABC, abstractmethod

from models.message import EmailModel


class SenderError(Exception):
    """Базовое исключение для ошибок."""


class Sender(ABC):
    @abstractmethod
    async def send(self, msg: EmailModel):
        """Отправка сообщения по email."""
