"""Модели рассылок."""

from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from models.notifications import TypeEnum


class ScheduledNotificationShort(BaseModel):
    """Сокращенная модель отложенной рассылки."""

    scheduled_id: UUID = Field(default_factory=uuid4)
    name: str
    timestamp_start: int | None
    cron: str | None
    type: TypeEnum = TypeEnum.email


class ScheduledNotificationFull(ScheduledNotificationShort):
    """Полная модель отложенной рассылки."""

    template_id: UUID
    users: list[UUID]
    data: dict
    enabled: bool = True
