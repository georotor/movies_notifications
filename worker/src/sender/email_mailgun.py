"""Модуль отправки сообщений через Mailgun."""

import logging

import aiohttp
import backoff

from models.message import EmailModel
from sender.abstract import Sender, SenderError

logger = logging.getLogger(__name__)


class MailgunSender(Sender):
    """Класс отправка сообщений через Mailgun."""

    def __init__(self, api_key: str, domain: str, from_email: str):
        """Инициализация объекта."""
        self.api_key = api_key
        self.domain = domain
        self.from_email = from_email

    @backoff.on_exception(backoff.expo, (SenderError, aiohttp.ClientError))
    async def send(self, msg: EmailModel) -> None:
        """Отправка сообщения через Mailgun."""
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                'https://api.mailgun.net/v3/{0}/messages'.format(self.domain),
                auth=aiohttp.BasicAuth('api', self.api_key),
                data={
                    'from': self.from_email,
                    'to': msg.to_email,
                    'subject': msg.subject,
                    'html': msg.body,
                },
            )

            if response.status != 200:
                logger.error('Error sending email: {0}'.format(await response.text()))
                raise SenderError('Error sending email: {0}'.format(await response.text()))

            logger.info('Send email send to {0}'.format(msg.to_email))
