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
    content: str
    event: EventEnum | None
    type: TypeEnum = TypeEnum.email

    @validator('content')
    def validate_content(cls, content):
        try:
            Environment().parse(content)
        except TemplateSyntaxError as e:
            raise HTTPException(status_code=400, detail='Invalid template content: {0}'.format(e))

        return content
