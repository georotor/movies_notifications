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

    async def scheduled(self, incoming_message: dict):
        if 'notification_id' not in incoming_message:
            logger.error('Invalid incoming scheduling message {0}'.format(incoming_message))
            return

        notify = await self._get_notification(UUID(incoming_message['notification_id']))
        if notify is None:
            logger.error('Scheduled notification {0} not found'.format(incoming_message['notification_id']))
            return

        if len(notify.sub_notifications) == 0:
            notify.sub_notifications = await self._create_sub_notifications(notify)

        for notification_id, timezone in notify.sub_notifications:
            run_date = await self._get_run_date_local(notify.timestamp_start, timezone)
            if run_date.timestamp() < datetime.now().timestamp():
                logger.warning('Notification {0} skipped, run_date: {1} current: {2}'.format(
                    notification_id,
                    run_date,
                    datetime.now()
                ))
                continue
            await self.scheduler.add(
                task_id=notification_id,
                run_date=run_date,
                args=(BrokerMessage(notification_id=notification_id), '{}.send'.format(notify.type.value))
            )
            logger.info('Notification {0} added to scheduler with run_date: {1}'.format(notification_id, run_date))

    async def remove(self, incoming_message: dict):
        if 'notification_id' not in incoming_message:
            logger.error('Invalid incoming removing message {0}'.format(incoming_message))
            return

        await self.scheduler.remove(UUID(incoming_message['notification_id']))

    async def _create_sub_notifications(self, notify: ScheduledNotification) -> list[tuple[UUID, str]] | None:
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
        doc = await self.db.get_one('scheduled_notifications', {'scheduled_id': notification_id, 'enabled': True})
        if doc:
            return ScheduledNotification(**doc)
        return None

    @staticmethod
    async def _get_run_date_local(timestamp: int, timezone: str) -> datetime:
        local_timezone = str(get_localzone())
        dt = datetime.fromtimestamp(timestamp)
        dt = dt.replace(tzinfo=ZoneInfo(key=timezone))
        dt = dt.astimezone(ZoneInfo(key=local_timezone))

        return dt

    @staticmethod
    async def _get_user_with_timezone(users: list, timezone: str) -> list:
        users_with_timezone = []
        for user in filter(lambda x: x['timezone'] == timezone, users):
            users_with_timezone.append(user['user_id'])

        return users_with_timezone

