"""Реализация AbstractDBManager для MongoDB."""
import logging
from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from core.config import settings
from db.mongo import get_mongo
from db.managers.abstract import AbstractDBManager, DBManagerError

logger = logging.getLogger(__name__)


class MongoManager(AbstractDBManager):
    """Реализация AbstractDBManager для MongoDB."""

    def __init__(self, client, db_name):
        """Конструктор класса."""
        self.db = client[db_name]

    async def get(self, table: str, query: dict, skip: int = 0, limit: int = 10):
        """Выборка списка документов из БД."""
        collection = self._open_collection(table)
        docs = []

        async for doc in collection.find(query).skip(skip).limit(limit):
            docs.append(doc)

        return docs

    async def get_one(self, table: str, query: dict):
        """Выборка одного документа из БД."""
        collection = self._open_collection(table)
        return await collection.find_one(query)

    async def update_one(self, table: str, query: dict, doc: dict):
        """Обновление одного документа в БД."""
        collection = self._open_collection(table)
        return await collection.update_one(query, {'$set': doc})

    async def delete_one(self, table: str, query: dict):
        """Удаление документа из БД."""
        collection = self._open_collection(table)
        return await collection.delete_one(query)

    async def delete_many(self, table: str, query: dict):
        """Удаление документов из БД."""
        collection = self._open_collection(table)
        return await collection.delete_many(query)

    async def save(self, table: str, obj_data: dict):
        """Создание записи в БД."""
        collection = self._open_collection(table)
        try:
            return await collection.insert_one(obj_data)
        except DuplicateKeyError as err:
            raise DBManagerError(str(err))

    def _open_collection(self, collection_name: str):
        """Переходим к нужной коллекции.

        :param collection_name: Название коллекции
        """
        return self.db[collection_name]


@lru_cache
def get_db_manager(client: AsyncIOMotorClient = Depends(get_mongo)) -> AbstractDBManager:
    """DI для FastAPI. Получаем менеджер для MONGO."""
    return MongoManager(client=client, db_name=settings.mongo_db)
