"""Модуль отправки сообщений через SendGrid."""

import logging
from http import HTTPStatus

import backoff
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from python_http_client.exceptions import BadRequestsError

from models.message import EmailModel
from sender.abstract import Sender, SenderError

logger = logging.getLogger(__name__)


class SendGridEmailSender(Sender):
    """Класс отправка сообщений через SendGrid."""

    def __init__(self, api_key: str, from_email: str):
        """Инициализация объекта."""
        self.sg_client = SendGridAPIClient(api_key)
        self.from_email = from_email

    @backoff.on_exception(backoff.expo, (SenderError, BadRequestsError))
    async def send(self, msg: EmailModel) -> None:
        """Отправка сообщения через SendGrid."""
        message = Mail(
            from_email=self.from_email,
            to_emails=msg.to_email,
            subject=msg.subject,
            html_content=msg.body,
        )

        response = await self.sg_client.send(message)

        if response.status_code != HTTPStatus.OK:
            logger.error('Failed to send email: {0}'.format(response.body))
            raise SenderError('Failed to send email: {0}'.format(response.body))

        logger.info('Send Email to {0}'.format(msg.to_email))
