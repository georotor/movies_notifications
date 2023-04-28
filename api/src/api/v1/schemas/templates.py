"""Модели шаблонов."""

from uuid import UUID
from pydantic import BaseModel


from models.notifications import EventEnum, TypeEnum


class TemplateShort(BaseModel):
    """Сокращенная модель шаблона."""

    template_id: UUID
    name: str
    event: EventEnum | None
    type: TypeEnum


class TemplateFull(TemplateShort):
    """Полная модель шаблона."""

    subject: str | None
    content: str
