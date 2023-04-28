"""Модуль управления отложенными рассылками в хранилище."""

from abc import ABC, abstractmethod


class DBManager(ABC):
    """Класс управления отложенными рассылками в хранилище."""

    @abstractmethod
    async def find(self, table: str, query: dict):
        """Поиск документов в таблице."""

    @abstractmethod
    async def get_one(self, table: str, query: dict):
        """Выборка одного документа из БД."""

    @abstractmethod
    async def insert_one(self, table: str, obj_data: dict):
        """Создание записи в БД."""

    @abstractmethod
    async def update_one(self, table: str, query: dict, doc: dict):
        """Обновление одного документа в БД."""
