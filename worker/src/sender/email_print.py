from sender.abstract import Sender

from models.message import EmailModel


class PrintEmailSender(Sender):
    def __init__(self, from_email: str):
        self.from_email = from_email

    async def send(self, msg: EmailModel) -> None:
        message = {
            'from_email': self.from_email,
            'to_emails': msg.to_email,
            'subject': msg.subject,
            'html_content': msg.body,
        }

        print(message)
