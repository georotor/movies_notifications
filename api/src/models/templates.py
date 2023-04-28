"""Модели шаблонов."""

from uuid import UUID, uuid4

from fastapi import HTTPException
from jinja2 import TemplateSyntaxError, Environment
from pydantic import BaseModel, Field, validator

from models.notifications import EventEnum, TypeEnum


class Template(BaseModel):
    """Модель шаблона."""

    template_id: UUID = Field(default_factory=uuid4)
    name: str
    event: EventEnum | None
    type: TypeEnum = TypeEnum.email
    subject: str | None
    content: str

    @validator('subject', always=True)
    def validate_subject(cls, subject, values):
        """Проверка корректности поля subject."""
        if values.get('type') == TypeEnum.email and not subject:
            raise HTTPException(status_code=400, detail='Subject field is required for email type')

        if subject:
            try:
                Environment().parse(subject)
            except TemplateSyntaxError as err:
                raise HTTPException(status_code=400, detail='Invalid template subject: {0}'.format(err))

        return subject

    @validator('content')
    def validate_content(cls, content):
        """Проверка корректности поля content."""
        try:
            Environment().parse(content)
        except TemplateSyntaxError as err:
            raise HTTPException(status_code=400, detail='Invalid template content: {0}'.format(err))

        return content
