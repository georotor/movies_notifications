import logging
from bson import ObjectId
from uuid import UUID

from db.abstract import DBManager

from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


class MongoDBManager(DBManager):
    def __init__(self, uri: str, database_name: str):
        self.client = AsyncIOMotorClient(uri, uuidRepresentation='standard')
        self.database = self.client[database_name]
        self.templates = self.database['templates']
        self.notifications = self.database['notifications']
        self.scheduled = self.database['scheduled']

    async def get_one(self, table: str, query: dict):
        """Выборка одного документа из БД."""
        return await self.database[table].find_one(query)

    async def insert_one(self, table: str, obj_data: dict):
        """Создание записи в БД."""
        return await self.database[table].insert_one(obj_data)

    async def update_one(self, table: str, query: dict, doc: dict):
        """Обновление одного документа в БД."""
        return await self.database[table].update_one(query, {"$set": doc})

    async def get_template_by_id(self, template_id: str) -> dict:
        template = await self.templates.find_one({"_id": ObjectId(template_id)})
        return template

    async def get_template_by_event_type(self, event: str, type: str) -> dict:
        template = await self.templates.find_one({
            'event': event,
            'type': type
        })
        return template

    async def set_notifications_status(self, notification_id: UUID, status: str):
        result = await self.notifications.update_one(
            {'notification_id': notification_id},
            {'$set': {'status': status}}
        )

        if result.modified_count == 1:
            logger.info('Notifications {0} set status: {1}'.format(notification_id, status))
        else:
            logger.error('Notifications {0} not found'.format(notification_id))