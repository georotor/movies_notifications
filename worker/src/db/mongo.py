"""Модуль для управления уведомлениями в Mongo."""

import logging
from uuid import UUID
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from db.abstract import DBManager

logger = logging.getLogger(__name__)


class MongoDBManager(DBManager):
    """Класс для управления уведомлениями в Mongo."""

    def __init__(self, uri: str, database_name: str):
        """Инициализация объекта для работы с Mongo."""
        self.client = AsyncIOMotorClient(uri, uuidRepresentation='standard')
        self.database = self.client[database_name]

    async def get_template_by_id(self, template_id: UUID) -> dict | None:
        """Поиск шаблона по его id."""
        return await self.database['templates'].find_one({'template_id': template_id})

    async def get_template_by_event_type(self, event: str, notify_type: str) -> dict:
        """Поиск шаблона по типу события и типу уведомления."""
        return await self.database['templates'].find_one({
            'event': event,
            'type': notify_type,
        })

    async def get_notification_by_id(self, notification_id: UUID) -> dict | None:
        """Поиск актуального, включенного и не выполненного уведомления."""
        pipeline = [
            {
                '$match': {'notification_id': notification_id},
            }, {
                '$lookup': {
                    'from': 'scheduled_notifications',
                    'localField': 'scheduled_id',
                    'foreignField': 'scheduled_id',
                    'as': 'scheduled',
                },
            }, {
                '$match': {'$or': [{'status': {'$ne': 'Ok'}}, {'scheduled.enabled': True}]},
            },
        ]
        notify = None
        async for doc in self.database['notifications'].aggregate(pipeline):
            notify = doc

        return notify

    async def set_notifications_status(self, notification_id: UUID, status: str):
        """Установка статуса и времени последнего обновления для уведомления."""
        result_db = await self.database['notifications'].update_one(
            {'notification_id': notification_id},
            {'$set': {'status': status, 'last_update': datetime.utcnow()}},
        )

        if result_db.modified_count == 1:
            logger.info('Notifications {0} set status: {1}'.format(notification_id, status))
        else:
            logger.error('Notifications {0} not found'.format(notification_id))
