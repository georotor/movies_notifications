"""Сервис управления отложенными уведомлениями."""

import logging
from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from core.config import settings
from db.managers.abstract import AbstractDBManager, AbstractBrokerManager, DBManagerError
from db.managers.mongo import get_db_manager
from db.managers.rabbit import get_broker_manager
from models.base import BrokerMessage
from models.notifications import Event, Notification, ScheduledNotification

logger = logging.getLogger(__name__)


class NotificationError(Exception):
    """Базовый класс для ошибок сервиса."""


class Notifications:
    """Класс управления отложенными уведомлениями."""

    def __init__(self, db: AbstractDBManager, rabbit: AbstractBrokerManager):
        """Инициализация объекта."""
        self.db = db
        self.rabbit = rabbit

    async def send(self, event: Event):
        """Записываем в базу неотложное уведомление и отправляем в очередь на отправку."""
        notification = Notification(**event.dict())

        if notification.template_id:
            template = await self.db.get_one('templates', {'template_id': notification.template_id})
            if not template:
                logger.warning('For notification {0} not found template {1}'.format(
                    notification.notification_id,
                    notification.template_id,
                ))
                raise NotificationError('Template {0} not found'.format(notification.template_id))

        await self.db.save('notifications', notification.dict())
        await self.rabbit.publish(
            BrokerMessage(**notification.dict()),
            routing_key='{0}.send'.format(event.type.value),
            priority=settings.notification_high_priority
        )

        logger.info('Notifications {0} published'.format(notification.notification_id))

    async def create(self, notification: ScheduledNotification) -> ScheduledNotification:
        """Сохраняет и отправляет в планировкщик отложенную рассылку."""
        template = await self.db.get_one('templates', {'template_id': notification.template_id})
        if not template:
            logger.warning('Not found template {0} for scheduled notification {1}'.format(
                notification.template_id,
                notification.scheduled_id
            ))
            raise NotificationError('Template {0} not found'.format(notification.template_id))

        try:
            await self.db.save('scheduled_notifications', notification.dict())
        except DBManagerError as err:
            logger.warning(str(err))
            raise NotificationError(str(err))

        if notification.enabled:
            await self.rabbit.publish(
                BrokerMessage(notification_id=notification.scheduled_id),
                routing_key='notification.scheduled'
            )
            logger.info('Scheduled notification {0} published'.format(notification.scheduled_id))

        return notification

    async def remove(self, scheduled_id: UUID):
        """Удаление запланированной рассылки."""
        notify_doc = await self.db.get_one('scheduled_notifications', {'scheduled_id': scheduled_id})
        if not notify_doc:
            logger.warning('Not found scheduled notifications {0}'.format(scheduled_id))
            raise NotificationError('Scheduled notifications {0} not found'.format(scheduled_id))

        notify = ScheduledNotification.parse_obj(notify_doc)

        for notification_id, _ in notify.sub_notifications:
            await self.rabbit.publish(
                BrokerMessage(notification_id=notification_id),
                routing_key='notification.remove'
            )
            logger.info('Notification {0} for scheduled {1} publish on removed'.format(
                notification_id,
                scheduled_id
            ))

        await self.db.delete_many('notifications', {'scheduled_id': scheduled_id})
        await self.db.delete_many('scheduled_notifications', {'scheduled_id': scheduled_id})

        logger.info('Scheduled notifications {0} removed'.format(scheduled_id))

    async def update(self, notify_new: ScheduledNotification):
        """Обновление запланированной рассылки."""
        notify_old_doc = await self.db.get_one('scheduled_notifications', {'scheduled_id': notify_new.scheduled_id})
        if not notify_old_doc:
            logger.warning('Not found scheduled notifications {0}'.format(notify_new.scheduled_id))
            raise NotificationError('Scheduled notifications {0} not found'.format(notify_new.scheduled_id))

        template = await self.db.get_one('templates', {'template_id': notify_new.template_id})
        if not template:
            logger.warning('Not found template {0} for scheduled notification {1}'.format(
                notify_new.template_id,
                notify_new.scheduled_id
            ))
            raise NotificationError('Template {0} not found'.format(notify_new.template_id))

        notify_old = ScheduledNotification.parse_obj(notify_old_doc)
        notify_new.sub_notifications = []
        await self.db.update_one(
            'scheduled_notifications',
            {'scheduled_id': notify_new.scheduled_id},
            notify_new.dict(exclude={'scheduled_id': True}),
        )

        for notification_id, _ in notify_old.sub_notifications:
            await self.rabbit.publish(
                BrokerMessage(notification_id=notification_id),
                routing_key='notification.remove',
            )
            logger.info('Notification {0} for scheduled {1} publish on removed'.format(
                notification_id,
                notify_new.scheduled_id,
            ))

        if notify_new.enabled:
            await self.rabbit.publish(
                BrokerMessage(notification_id=notify_new.scheduled_id),
                routing_key='notification.scheduled',
            )
            logger.info('Scheduled notification {0} published'.format(notify_new.scheduled_id))


@lru_cache()
def get_notification_service(
        db: AbstractDBManager = Depends(get_db_manager),
        rabbit: AbstractBrokerManager = Depends(get_broker_manager),
) -> Notifications:
    """Получение сервиса для DI."""
    return Notifications(db, rabbit)
