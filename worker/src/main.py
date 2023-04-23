import asyncio
from logging import config as logging_config

from auth.user import UserData
from broker.rabbit import Rabbit
from db.mongo import MongoDBManager
from core.config import settings
from core.logger import LOGGING
from message.email import EmailMessage
#from sender.email_print import PrintEmailSender
#from sender.email_sendgrid import SendGridEmailSender
from sender.email_mailgun import MailgunSender

logging_config.dictConfig(LOGGING)


async def start():
    broker = Rabbit(settings.rabbit_uri)
    db = MongoDBManager(settings.mongo_uri, settings.mongo_db)
    auth = UserData(settings.auth_url)

    #email_sender = SendGridEmailSender(settings.sendgrid_api_key, settings.sendgrid_from_email)
    #email_sender = PrintEmailSender(settings.sendgrid_from_email)
    email_sender = MailgunSender(settings.mailgun_api_key, settings.mailgun_domain, settings.mailgun_from_email)
    email_message = EmailMessage(db, email_sender, auth)

    email_queue = await broker.get_queue(settings.rabbit_queue)

    await broker.consume(email_queue, email_message.handle)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.run_forever()
