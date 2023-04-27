from uuid import UUID

from pydantic import BaseModel

from models.base import EventEnum, TypeEnum


class Notification(BaseModel):
    notification_id: UUID
    scheduled_id: UUID | None = None
    template_id: UUID | None
    event: EventEnum | None
    type: TypeEnum = TypeEnum.email
    users: list[UUID]
    data: dict
    status: str | None
