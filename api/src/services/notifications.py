import logging
from functools import lru_cache

from fastapi import Depends

from db.managers.abstract import AbstractDBManager, AbstractBrokerManager, DBManagerError
from db.managers.mongo import get_db_manager
from db.managers.rabbit import get_broker_manager
from models.schemas import Event, BrokerMessage, Notification, ScheduledNotification

logger = logging.getLogger(__name__)


class NotificationError(Exception):
    """Базовый класс для ошибок сервиса."""


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

    async def scheduled(self, notification: ScheduledNotification):
        template = await self.db.get_one('templates', {'template_id': notification.template_id})
        if not template:
            logger.warning('Not found template {0} for scheduled notification {1}'.format(
                notification.template_id,
                notification.scheduled_id
            ))
            raise NotificationError('Template {0} not found'.format(notification.template_id))

        try:
            await self.db.save('scheduled_notifications', notification.dict())
        except DBManagerError as e:
            logger.warning(str(e))
            raise NotificationError(str(e))

        if notification.enabled:
            await self.rabbit.publish(
                BrokerMessage(notification_id=notification.scheduled_id),
                routing_key='notification.scheduled'
            )
            logger.info('Scheduled notification {0} published'.format(notification.scheduled_id))


@lru_cache()
def get_notification_service(
        db: AbstractDBManager = Depends(get_db_manager),
        rabbit: AbstractBrokerManager = Depends(get_broker_manager)
) -> Notifications:
    return Notifications(db, rabbit)
