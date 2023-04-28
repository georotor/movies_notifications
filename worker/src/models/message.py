"""Модели уведомлений."""

from pydantic import BaseModel, EmailStr


class EmailModel(BaseModel):
    """Модель для уведомления email."""

    to_email: EmailStr
    subject: str
    body: str
