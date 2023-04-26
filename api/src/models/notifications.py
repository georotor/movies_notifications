from enum import Enum
from uuid import UUID, uuid4
from typing import Optional

from cron_validator import CronValidator
from fastapi import HTTPException
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
    sub_notifications: Optional[list[tuple[UUID, str]]] = []

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
