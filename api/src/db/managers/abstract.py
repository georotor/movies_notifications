"""Описание интерфейса для работы с БД."""
from abc import ABC, abstractmethod

from models.schemas import Notification

class DBManagerError(Exception):
    """Базовое исключение для ошибок в работе менеджера БД."""


class AbstractDBManager(ABC):
    """Простой менеджер для работы с БД."""

    @abstractmethod
    async def get(self, table: str, query: dict, skip: int = 0, limit: int = 10):
        """Выборка списка документов из БД."""

    @abstractmethod
    async def get_one(self, table: str, query: dict):
        """Выборка одного документа из БД."""

    @abstractmethod
    async def update_one(self, table: str, id: str, doc: dict):
        """Обновление одного документа в БД по его _id."""

    @abstractmethod
    async def delete_one(self, table: str, id: str):
        """Удаление документа из БД по его _id."""

    @abstractmethod
    async def save(self, table: str, obj_data: dict):
        """Создание записи в БД.

        Args:
          table: название таблицы (коллекции) БД;
          obj_data: словарь с данными для поиска.

        """


class AbstractBrokerManager(ABC):
    """Простой менеджер для работы с Брокером."""

    @abstractmethod
    async def publish(self, msg: Notification, routing_key: str):
        """Публикация сообщения в брокере."""
