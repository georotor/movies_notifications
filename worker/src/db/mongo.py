import logging
from uuid import UUID
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from db.abstract import DBManager

logger = logging.getLogger(__name__)


class MongoDBManager(DBManager):
    def __init__(self, uri: str, database_name: str):
        self.client = AsyncIOMotorClient(uri, uuidRepresentation='standard')
        self.database = self.client[database_name]

    async def get_template_by_id(self, template_id: UUID) -> dict | None:
        return await self.database['templates'].find_one({'template_id': template_id})

    async def get_template_by_event_type(self, event: str, type: str) -> dict:
        return await self.database['templates'].find_one({
            'event': event,
            'type': type
        })

    async def get_notification_by_id(self, notification_id: UUID) -> dict | None:
        pipeline = [
            {
                "$lookup": {
                    "from": "scheduled_notifications",
                    "localField": "scheduled_id",
                    "foreignField": "scheduled_id",
                    "as": "scheduled"
                }
            }, {
                "$match": {
                    "$and": [
                        {"notification_id": notification_id},
                        {"$or": [{"status": {"$ne": "Ok"}}, {"scheduled.enabled": True}]}
                    ]
                }
            }
        ]
        result = None
        async for doc in self.database['notifications'].aggregate(pipeline):
            result = doc

        return result

    async def set_notifications_status(self, notification_id: UUID, status: str):
        result = await self.database['notifications'].update_one(
            {'notification_id': notification_id},
            {'$set': {'status': status, 'last_update': datetime.utcnow()}}
        )

        if result.modified_count == 1:
            logger.info('Notifications {0} set status: {1}'.format(notification_id, status))
        else:
            logger.error('Notifications {0} not found'.format(notification_id))