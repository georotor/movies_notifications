"""Воркер отправки email сообщений."""

import asyncio
from logging import config as logging_config

from auth.user import UserData
from broker.rabbit import Rabbit
from core.config import settings
from core.logger import LOGGING
from db.mongo import MongoDBManager
from message.email import EmailMessage
from sender.abstract import Sender
from sender.email_print import PrintEmailSender
from sender.email_sendgrid import SendGridEmailSender
from sender.email_mailgun import MailgunSender

logging_config.dictConfig(LOGGING)


async def get_sender(sender_name: str) -> Sender:
    """Возвращает объект отправки сообщений."""
    match sender_name:
        case 'print':
            return PrintEmailSender(settings.sendgrid_from_email)
        case 'sendgrid':
            return SendGridEmailSender(settings.sendgrid_api_key, settings.sendgrid_from_email)
        case 'mailgun':
            MailgunSender(settings.mailgun_api_key, settings.mailgun_domain, settings.mailgun_from_email)
        case _:
            raise ValueError('Sender {0} not found'.format(sender_name))


async def start():
    """Запуск воркера."""
    broker = Rabbit(settings.rabbit_uri)
    db = MongoDBManager(settings.mongo_uri, settings.mongo_db)
    auth = UserData(settings.auth_url, settings.auth_url_list, settings.auth_authorization)

    email_sender = await get_sender(settings.sender)
    email_message = EmailMessage(db, email_sender, auth)

    await broker.consume(settings.rabbit_queue, email_message.handle)

    try:
        await asyncio.Future()
    finally:
        await broker.close()


if __name__ == '__main__':
    asyncio.run(start())
