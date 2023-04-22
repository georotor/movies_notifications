from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from sender.abstract import Sender


class SendGridEmailSender(Sender):
    def __init__(self, api_key: str, from_email: str):
        self.sg_client = SendGridAPIClient(api_key)
        self.from_email = from_email

    async def send(self, to_email: str, subject: str, content: str) -> None:
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=content,
        )

        response = await self.sg_client.send(message)

        if response.status_code // 100 != 2:
            raise Exception(f"Failed to send email: {response.body}")
