"""Описание интерфейса для работы с БД."""
from abc import ABC, abstractmethod

from models.schemas import Notification

class DBManagerError(Exception):
    """Базовое исключение для ошибок в работе менеджера БД."""


class AbstractDBManager(ABC):
    """Простой менеджер для работы с БД."""

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
    async def publish(self, msg: Notification):
        """Публикация сообщения в брокере.

        :param msg:
        :return:
        """
