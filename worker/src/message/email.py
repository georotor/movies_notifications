import json

from aio_pika import IncomingMessage
from jinja2 import Template

from db.abstract import DBManager
from message.abstarct import Message
from sender.abstract import Sender


class EmailMessage(Message):
    def __init__(self, db: DBManager, email_sender: Sender):
        self.db = db
        self.email_sender = email_sender

    async def handle(self, message: IncomingMessage) -> tuple[str, str, dict]:
        payload = message.body.decode()
        context = json.loads(payload)

        template = await self.db.get_template(context['template_id'])
        jinja_template = Template(template['content'])

        rendered_content = jinja_template.render(context['variables'])

        to_email = context['to_email']
        subject = context['subject']

        await self.email_sender.send(to_email, subject, rendered_content)

        await message.ack()

        return subject, to_email, context['variables']
