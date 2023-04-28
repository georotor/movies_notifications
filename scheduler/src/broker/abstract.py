"""Модуль работы с брокером."""

from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel


class Broker(ABC):
    """Класс работы с брокером."""

    @abstractmethod
    async def close(self):
        """Закрытие соединения."""

    @abstractmethod
    async def consume(self, queue, callback):
        """Обработка входящих сообщений."""

    @abstractmethod
    async def publish(self, exchange_name: str, msg: Type[BaseModel], routing_key: str):
        """Публикация сообщения в брокере."""
