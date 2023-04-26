from enum import Enum
from uuid import UUID, uuid4

from cron_validator import CronValidator
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
    template_id: UUID = Field(default_factory=uuid4)
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


class ScheduledNotification(BaseModel):
    scheduled_id: UUID = Field(default_factory=uuid4)
    name: str
    timestamp_start: int | None
    cron: str | None
    type: TypeEnum = TypeEnum.email
    template_id: UUID
    users: list[UUID]
    data: dict
    enabled: bool = True

    @validator('cron', always=True)
    def validate_subject(cls, cron, values):
        if not values.get('timestamp_start') and not cron:
            raise HTTPException(status_code=400, detail='Must be one of the fields timestamp_start or cron')

        if cron:
            try:
                CronValidator.parse(cron)
            except ValueError as e:
                raise HTTPException(status_code=400, detail='Invalid field cron: {0}'.format(e))

        return cron


class BrokerMessage(BaseModel):
    notification_id: UUID


class SubScheduledNotification:
    pass