from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class BrokerMessage(BaseModel):
    notification_id: UUID


class EventEnum(str, Enum):
    registered = 'registered'


class TypeEnum(str, Enum):
    email = 'email'
    sms = 'sms'
