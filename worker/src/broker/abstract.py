"""Модуль работы с брокером."""

from abc import ABC, abstractmethod
from typing import Any, Callable


class Broker(ABC):
    """Класс работы с брокером."""

    @abstractmethod
    async def close(self):
        """Закрытие соединения."""

    @abstractmethod
    async def consume(self, queue_name: str, callback: Callable[[dict], Any]):
        """Обработка входящего сообщения."""
