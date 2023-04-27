import logging
import json
from uuid import UUID

from aio_pika import IncomingMessage
from jinja2 import Template

from auth.abstract import Auth
from db.abstract import DBManager
from message.abstarct import Message
from sender.abstract import Sender

logger = logging.getLogger(__name__)


class EmailMessage(Message):
    def __init__(self, db: DBManager, email_sender: Sender, user_data: Auth):
        self.db = db
        self.email_sender = email_sender
        self.user_data = user_data

    async def handle(self, context: dict):
        template = await self._get_template(context)
        if template is None:
            logger.error('{0} - Template not found for notifications'.format(context['notification_id']))
            await self.db.set_notifications_status(UUID(context['notification_id']), 'Error: Template not found')
            return

        jinja_subject = Template(template['subject'])
        jinja_body = Template(template['content'])

        for user_id in context['users']:
            context['user'] = await self.user_data.get(UUID(user_id))
            if context['user'] is None:
                logger.warning('{0} - User {1} not found'.format(context['notification_id'], user_id))
                continue

            subject = jinja_subject.render({**context['user'], **context['data']})
            body = jinja_body.render({**context['user'], **context['data']})

            to_email = context['user']['email']

            await self.email_sender.send(to_email, subject, body)

            logger.info('{0} - Send email'.format(context['notification_id']))
            await self.db.set_notifications_status(UUID(context['notification_id']), 'Ok')


    async def _get_template(self, context: dict):
        if 'data' in context and 'template_id' in context['data']:
            return await self.db.get_template_by_id(context['data']['template_id'])

        if context.get('event') is not None:
            if context.get('type') is not None:
                return await self.db.get_template_by_event_type(context['event'], context['type'])

        return None
