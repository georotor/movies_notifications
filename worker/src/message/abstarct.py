"""Модуль отправки уведомлений."""

from abc import ABC, abstractmethod


class Message(ABC):
    """Класс отправки уведомлений."""

    @abstractmethod
    async def handle(self, context: dict):
        """Отправка уведомления по сообщению из брокера."""
