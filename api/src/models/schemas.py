from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TypeEnum(str, Enum):
    email = 'email'
    sms = 'sms'


class Event(BaseModel):
    event: str
    type: TypeEnum = TypeEnum.email
    users: list[UUID]
    data: dict


class Notification(Event):
    notification_id: UUID = Field(default_factory=uuid4)
