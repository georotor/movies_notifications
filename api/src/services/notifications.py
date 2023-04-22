import logging
from functools import lru_cache

from fastapi import Depends

from db.managers.abstract import AbstractDBManager, AbstractBrokerManager
from db.managers.mongo import get_db_manager
from db.managers.rabbit import get_broker_manager
from models.schemas import Event, Notification

logger = logging.getLogger(__name__)


class Notifications:

    def __init__(self, db: AbstractDBManager, rabbit: AbstractBrokerManager):
        self.db = db
        self.rabbit = rabbit

    async def send(self, event: Event):
        """Записываем в базу и отправляем в очередь."""
        notification = Notification(**event.dict())

        await self.db.save('notifications', notification.dict())
        await self.rabbit.publish(notification, routing_key='{0}.send'.format(event.type.value))

        logger.info('Notifications {0} published'.format(notification.notification_id))


@lru_cache()
def get_notification_service(
        db: AbstractDBManager = Depends(get_db_manager),
        rabbit: AbstractBrokerManager = Depends(get_broker_manager)
) -> Notifications:
    return Notifications(db, rabbit)
