"""Модуль отправки email сообщений."""

from abc import ABC, abstractmethod

from models.message import EmailModel


class SenderError(Exception):
    """Базовое исключение для ошибок."""


class Sender(ABC):
    """Класс отправка email сообщений."""

    @abstractmethod
    async def send(self, msg: EmailModel):
        """Отправка сообщения по email."""
