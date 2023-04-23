from sender.abstract import Sender


class PrintEmailSender(Sender):
    def __init__(self, from_email: str):
        self.from_email = from_email

    async def send(self, to_email: str, subject: str, content: str) -> None:
        message = {
            'from_email': self.from_email,
            'to_emails': to_email,
            'subject': subject,
            'html_content': content,
        }

        print(message)
