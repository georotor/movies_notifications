"""Модели шаблонов."""

from uuid import UUID

from pydantic import BaseModel, validator

from models.base import EventEnum, TypeEnum


class Template(BaseModel):
    """Модель шаблонов."""

    template_id: UUID
    name: str
    event: EventEnum | None
    type: TypeEnum = TypeEnum.email
    subject: str | None
    content: str

    @validator('subject', always=True)
    def validate_subject(cls, subject, values):
        """Проверка что тема сообщения заполнена для email."""
        if values.get('type') == TypeEnum.email and subject is None:
            raise ValueError('Subject required for type email')
        return subject
