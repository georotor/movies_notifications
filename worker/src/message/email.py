"""Модуль отправки email уведомлений."""

import logging
from uuid import UUID

from jinja2 import Template as TemplateJinja

from auth.abstract import Auth, AuthError
from db.abstract import DBManager
from message.abstarct import Message
from models.user import User
from models.message import EmailModel
from models.notifications import Notification
from models.templates import Template
from sender.abstract import Sender

logger = logging.getLogger(__name__)


class EmailMessage(Message):
    """Класс отправки email уведомлений."""

    def __init__(self, db: DBManager, email_sender: Sender, user_data: Auth):
        """Инициализация объекта."""
        self.db = db
        self.email_sender = email_sender
        self.user_data = user_data

    async def handle(self, context: dict):
        """Отправка уведомления по сообщению из брокера."""
        notify = await self._get_notification(context)
        if notify is None:
            logger.error('Notification {0} not found or disabled')
            return

        template = await self._get_template(notify)
        if template is None:
            logger.error('Template not found for notifications {0}'.format(notify.notification_id))
            await self.db.set_notifications_status(notify.notification_id, 'Error: Template not found')
            return

        jinja_subject = TemplateJinja(template.subject)
        jinja_body = TemplateJinja(template.content)

        for user in await self._get_users_data(notify):
            if user.user_id not in notify.users:
                logger.warning('User {0} not in notification {1}'.format(user.user_id, notify.notification_id))
                continue

            notify.users.remove(user.user_id)

            mail = EmailModel(
                to_email=user.email,
                subject=jinja_subject.render({**user.dict(), **notify.data}),
                body=jinja_body.render({**user.dict(), **notify.data}),
            )

            await self.email_sender.send(mail)

            logger.info('Send email on {0} for notification {1}'.format(mail.to_email, notify.notification_id))

        if notify.users:
            logger.warning('Users {0} for notification {1} no found in Auth'.format(
                notify.users, notify.notification_id,
            ))

        await self.db.set_notifications_status(notify.notification_id, 'Ok')
        logger.info('Notification {0} done'.format(notify.notification_id))

    async def _get_users_data(self, notify: Notification) -> list[User]:
        users = []
        try:
            users = await self.user_data.get_list(notify.users)
        except AuthError as err:
            logger.error('Error get users for notification {0}: {1}'.format(notify.notification_id, err))

        users = [User.parse_obj(user) for user in users]

        return users

    async def _get_template(self, notify: Notification) -> Template | None:
        """Загрузка шаблона для уведомления."""
        if notify.template_id:
            template = await self.db.get_template_by_id(notify.template_id)
            try:
                return Template.parse_obj(template)
            except ValueError as err:
                logger.error('Template error for notification {0}: {1}'.format(notify.notification_id, err))

        if notify.event is not None and notify.type is not None:
            template = await self.db.get_template_by_event_type(notify.event.value, notify.type.value)
            return Template.parse_obj(template)

        return None

    async def _get_notification(self, context: dict) -> Notification | None:
        """Загрузка уведомления из БД."""
        if 'notification_id' in context:
            notify = await self.db.get_notification_by_id(UUID(context.get('notification_id')))
            if notify:
                return Notification.parse_obj(notify)

        return None
