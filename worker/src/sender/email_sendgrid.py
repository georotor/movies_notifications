import logging

import backoff
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from sender.abstract import Sender, SenderError
from python_http_client.exceptions import BadRequestsError

logger = logging.getLogger(__name__)


class SendGridEmailSender(Sender):
    def __init__(self, api_key: str, from_email: str):
        self.sg_client = SendGridAPIClient(api_key)
        self.from_email = from_email

    @backoff.on_exception(backoff.expo, (SenderError, BadRequestsError))
    async def send(self, to_email: str, subject: str, content: str) -> None:
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=content,
        )

        response = await self.sg_client.send(message)

        if response.status_code != 200:
            logger.error('Failed to send email: {0}'.format(response.body))
            raise SenderError('Failed to send email: {0}'.format(response.body))

        logger.info('Email <{0}> send to <{1}>'.format(subject, to_email))
