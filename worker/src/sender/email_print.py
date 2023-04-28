"""Модуль отображения email сообщений."""

from sender.abstract import Sender

from models.message import EmailModel


class PrintEmailSender(Sender):
    """Класс отображения email сообщений."""

    def __init__(self, from_email: str):
        """Инициализация объекта."""
        self.from_email = from_email

    async def send(self, msg: EmailModel) -> None:
        """Вывод сообщения."""
        message = {
            'from_email': self.from_email,
            'to_emails': msg.to_email,
            'subject': msg.subject,
            'html_content': msg.body,
        }

        print(message)
