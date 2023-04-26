from uuid import UUID
from typing import Optional

from pydantic import BaseModel

from models.notifications import TypeEnum


class ScheduledNotificationShort(BaseModel):
    scheduled_id: UUID
    name: str
    timestamp_start: int | None
    cron: str | None
    type: TypeEnum = TypeEnum.email


class ScheduledNotificationFull(ScheduledNotificationShort):
    template_id: UUID
    users: list[UUID]
    data: dict
    enabled: bool = True
