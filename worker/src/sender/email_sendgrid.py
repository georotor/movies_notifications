import logging

import backoff
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from python_http_client.exceptions import BadRequestsError

from models.message import EmailModel
from sender.abstract import Sender, SenderError

logger = logging.getLogger(__name__)


class SendGridEmailSender(Sender):
    def __init__(self, api_key: str, from_email: str):
        self.sg_client = SendGridAPIClient(api_key)
        self.from_email = from_email

    @backoff.on_exception(backoff.expo, (SenderError, BadRequestsError))
    async def send(self, msg: EmailModel) -> None:
        message = Mail(
            from_email=self.from_email,
            to_emails=msg.to_email,
            subject=msg.subject,
            html_content=msg.body,
        )

        response = await self.sg_client.send(message)

        if response.status_code != 200:
            logger.error('Failed to send email: {0}'.format(response.body))
            raise SenderError('Failed to send email: {0}'.format(response.body))

        logger.info('Send Email to {0}'.format(msg.to_email))
