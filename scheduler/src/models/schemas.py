from enum import Enum
from uuid import UUID, uuid4
from typing import Optional

from pydantic import BaseModel, Field


class EventEnum(str, Enum):
    registered = 'registered'


class TypeEnum(str, Enum):
    email = 'email'
    sms = 'sms'


class BaseNotification(BaseModel):
    template_id: UUID | None
    event: EventEnum | None
    type: TypeEnum = TypeEnum.email
    users: list[UUID]
    data: dict


class ScheduledNotification(BaseNotification):
    scheduled_id: UUID = Field(default_factory=uuid4)
    sub_notifications: Optional[list[UUID]] = []
    timestamp_start: int
    enabled: bool = True


class SubScheduledNotification(BaseNotification):
    notification_id: UUID = Field(default_factory=uuid4)
    scheduled_id: UUID


class BrokerMessage(BaseModel):
    notification_id: UUID
