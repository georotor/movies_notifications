"""Реализация AbstractDBManager для MongoDB."""
import logging
from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from db.mongo import get_mongo
from db.managers.abstract import AbstractDBManager

logger = logging.getLogger(__name__)


class MongoManager(AbstractDBManager):
    """Реализация AbstractDBManager для MongoDB."""

    def __init__(self, client, db_name):
        """Конструктор класса.

        :param client: Инициированное подключение к БД
        :param db_name: Название БД
        """
        self.db = client[db_name]

    async def save(self, table: str, obj_data: dict):
        """Создание записи в БД.

        :param table: Название таблицы (коллекции) БД
        :param obj_data: Словарь с данными для поиска
        """
        collection = self._open_collection(table)
        await collection.insert_one(obj_data)

    def _open_collection(self, collection_name: str):
        """Переходим к нужной коллекции.

        :param collection_name: Название коллекции
        """
        return self.db[collection_name]


@lru_cache
def get_db_manager(client: AsyncIOMotorClient = Depends(get_mongo)) -> AbstractDBManager:
    """DI для FastAPI. Получаем менеджер для MONGO."""
    return MongoManager(client=client, db_name=settings.mongo_db)
