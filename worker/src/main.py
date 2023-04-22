import asyncio
from logging import config as logging_config

from broker.rabbit import Rabbit
from db.mongo import MongoDBManager
from core.config import settings
from core.logger import LOGGING
from message.email import EmailMessage
from sender.email_sendgrid import SendGridEmailSender

logging_config.dictConfig(LOGGING)


async def start():
    email_sender = SendGridEmailSender(settings.sendgrid_api_key, settings.sendgrid_from_email)

    db = MongoDBManager(settings.mongo_uri, settings.mongo_db)

    rabbit_conn = Rabbit(settings.rabbit_uri)
    queue = await rabbit_conn.get_queue(settings.rabbit_queue)

    email_message = EmailMessage(db, email_sender)

    await rabbit_conn.consume(queue, email_message.handle)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.run_forever()
