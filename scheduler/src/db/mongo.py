"""Модуль управления отложенными рассылками в Mongo."""

import logging

from db.abstract import DBManager

from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


class MongoDBManager(DBManager):
    """Класс управления отложенными рассылками в Mongo."""

    def __init__(self, uri: str, database_name: str):
        """Инициализация объекта."""
        self.client = AsyncIOMotorClient(uri, uuidRepresentation='standard')
        self.database = self.client[database_name]

    async def find(self, table: str, query: dict):
        """Поиск документов в таблице."""
        docs = []
        async for doc in self.database[table].find(query):
            docs.append(doc)
        return docs

    async def get_one(self, table: str, query: dict):
        """Выборка одного документа из БД."""
        return await self.database[table].find_one(query)

    async def insert_one(self, table: str, obj_data: dict):
        """Создание записи в БД."""
        return await self.database[table].insert_one(obj_data)

    async def update_one(self, table: str, query: dict, doc: dict):
        """Обновление одного документа в БД."""
        return await self.database[table].update_one(query, {'$set': doc})
