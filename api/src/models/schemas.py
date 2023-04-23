from enum import Enum
from uuid import UUID, uuid4

from fastapi import HTTPException
from jinja2 import TemplateSyntaxError, Environment
from pydantic import BaseModel, Field, validator


class EventEnum(str, Enum):
    registered = 'registered'


class TypeEnum(str, Enum):
    email = 'email'
    sms = 'sms'


class Event(BaseModel):
    event: EventEnum
    type: TypeEnum = TypeEnum.email
    users: list[UUID]
    data: dict


class Notification(Event):
    notification_id: UUID = Field(default_factory=uuid4)


class Template(BaseModel):
    name: str
    event: EventEnum | None
    type: TypeEnum = TypeEnum.email
    subject: str | None
    content: str

    @validator('subject', always=True)
    def validate_subject(cls, subject, values):
        if values.get('type') == TypeEnum.email and not subject:
            raise HTTPException(status_code=400, detail='Subject field is required for email type')

        if subject:
            try:
                Environment().parse(subject)
            except TemplateSyntaxError as e:
                raise HTTPException(status_code=400, detail='Invalid template subject: {0}'.format(e))

        return subject

    @validator('content')
    def validate_content(cls, content):
        try:
            Environment().parse(content)
        except TemplateSyntaxError as e:
            raise HTTPException(status_code=400, detail='Invalid template content: {0}'.format(e))

        return content
