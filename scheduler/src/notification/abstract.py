from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel


class Notification(ABC):
    @abstractmethod
    async def init(self):
        """Загрузка запланированных уведомлений из БД и постановка их в планировщик."""

    @abstractmethod
    async def scheduled(self, message: Type[BaseModel]):
        """Обработка сообщение на постановку в планировщик."""

    @abstractmethod
    async def remove(self, incoming_message: dict):
        """Обработка сообщение на удаление задач."""
