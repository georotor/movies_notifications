import logging
from datetime import datetime
from uuid import UUID

from tzlocal import get_localzone
from zoneinfo import ZoneInfo

from auth.abstract import Auth
from db.abstract import DBManager
from notification.abstract import Notification
from models.schemas import ScheduledNotification, SubScheduledNotification, BrokerMessage
from scheduler.abstract import Scheduler

logger = logging.getLogger(__name__)


class Message(Notification):
    def __init__(self, db: DBManager, user: Auth, scheduler: Scheduler):
        self.db = db
        self.user = user
        self.scheduler = scheduler

    async def init(self):
        """Загрузка запланированных уведомлений из БД и постановка их в планировщик."""
        query = {
            "$or": [
                {"$and": [{"enabled": True}, {"timestamp_start": {"$gt": datetime.now().timestamp()}}]},
                {"$and": [{"enabled": True}, {"cron": {"$type": "string", "$exists": True, "$ne": ""}}]}
            ]
        }
        for notify in await self.db.find('scheduled_notifications', query):
            await self.scheduled(ScheduledNotification(**notify))

    async def incoming(self, incoming_message: dict):
        """Получаем сообщение, загружаем из БД уведомление и ставим его в очередь."""
        if not isinstance(incoming_message, dict):
            logger.error('Invalid incoming message {0}'.format(incoming_message))
            return

        if 'notification_id' not in incoming_message:
            logger.error('Invalid incoming scheduling message {0}'.format(incoming_message))
            return

        notify_id = incoming_message['notification_id']
        if isinstance(incoming_message['notification_id'], str):
            notify_id = UUID(incoming_message['notification_id'])

        notify = await self._get_notification(notify_id)
        if notify is None:
            logger.error('Scheduled notification {0} not found'.format(notify_id))
            return

        await self.scheduled(notify)

    async def scheduled(self, scheduled_notify: ScheduledNotification):
        """Разбиваем время выполнения по таймзонам и ставим на выполнение."""
        if len(scheduled_notify.sub_notifications) == 0:
            scheduled_notify.sub_notifications = await self._create_sub_notifications(scheduled_notify)
            await self.db.update_one(
                'scheduled_notifications',
                {'scheduled_id': scheduled_notify.scheduled_id},
                {'sub_notifications': scheduled_notify.sub_notifications}
            )

        for notify_id, timezone in scheduled_notify.sub_notifications:
            if scheduled_notify.timestamp_start:
                await self._scheduled_by_date(scheduled_notify, notify_id, timezone)
                continue

            await self._scheduled_by_cron(scheduled_notify, notify_id, timezone)

    async def _scheduled_by_cron(self, scheduled_notify: ScheduledNotification, notify_id: UUID, timezone: str):
        """Установка в планировщик периодической задачи по крону."""
        await self.scheduler.add_cron(
            task_id=notify_id,
            cron=scheduled_notify.cron,
            timezone=timezone,
            args=(BrokerMessage(notification_id=notify_id), '{}.send'.format(scheduled_notify.type.value))
        )
        logger.info('Scheduled notification {0} added to scheduler with cron: {1} for timezone {2}'.format(
            notify_id, scheduled_notify.cron, timezone
        ))

    async def _scheduled_by_date(self, scheduled_notify: ScheduledNotification, notify_id: UUID, timezone: str):
        """Установка в планировщик задачи по дате."""
        run_date = await self._get_run_date_local(scheduled_notify.timestamp_start, timezone)
        if run_date.timestamp() < datetime.now().timestamp():
            logger.warning('Scheduled notification {0} skipped, run_date: {1} current: {2}'.format(
                notify_id,
                run_date,
                datetime.now()
            ))
            return

        await self.scheduler.add(
            task_id=notify_id,
            run_date=run_date,
            args=(BrokerMessage(notification_id=notify_id), '{}.send'.format(scheduled_notify.type.value))
        )
        logger.info('Scheduled notification {0} added to scheduler with run_date: {1}'.format(
            notify_id, run_date
        ))

    async def remove(self, incoming_message: dict):
        """Удаляем уведомление из планировщика."""
        if 'notification_id' not in incoming_message:
            logger.error('Invalid incoming removing message {0}'.format(incoming_message))
            return

        await self.scheduler.remove(UUID(incoming_message['notification_id']))

    async def _create_sub_notifications(self, notify: ScheduledNotification) -> list[tuple[UUID, str]] | None:
        """Создаем уведомления для разных таймзон пользователей."""
        result = []
        users_list = await self.user.get_list(notify.users)
        timezones = set(item['timezone'] for item in users_list)

        for timezone in timezones:
            sub_notification = SubScheduledNotification.parse_obj({
                **notify.dict(),
                'users': await self._get_user_with_timezone(users_list, timezone),
                'scheduled_id': notify.scheduled_id
            })
            await self.db.insert_one('notifications', sub_notification.dict())
            result.append((sub_notification.notification_id, timezone))

        if len(result) > 0:
            return result

        return None

    async def _get_notification(self, notification_id: UUID) -> ScheduledNotification | None:
        """Загрузка уведомления из БД."""
        doc = await self.db.get_one('scheduled_notifications', {'scheduled_id': notification_id, 'enabled': True})
        if doc:
            return ScheduledNotification(**doc)
        return None

    @staticmethod
    async def _get_run_date_local(timestamp: int, timezone: str) -> datetime:
        """Рассчитывает локальное время выполнения уведомления для таймзоны получателя."""
        local_timezone = str(get_localzone())
        dt = datetime.fromtimestamp(timestamp)
        dt = dt.replace(tzinfo=ZoneInfo(key=timezone))
        dt = dt.astimezone(ZoneInfo(key=local_timezone))

        return dt

    @staticmethod
    async def _get_user_with_timezone(users: list, timezone: str) -> list:
        """Возвращает список пользователей с указанной таймзоной."""
        users_with_timezone = []
        for user in filter(lambda x: x['timezone'] == timezone, users):
            users_with_timezone.append(user['user_id'])

        return users_with_timezone
