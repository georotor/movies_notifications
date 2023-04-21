from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    event: str
    users: list[UUID]
    data: dict


class Notification(Event):
    notification_id: UUID = Field(default_factory=uuid4)
