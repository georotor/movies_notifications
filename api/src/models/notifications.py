"""Модели уведомлений."""

from enum import Enum
from uuid import UUID, uuid4
from typing import Optional

from cron_validator import CronValidator
from fastapi import HTTPException
from pydantic import BaseModel, Field, conlist, validator


class EventEnum(str, Enum):
    """Список доступных типов событий."""

    registered = 'registered'


class TypeEnum(str, Enum):
    """Список доступных типов рассылок."""

    email = 'email'


class Event(BaseModel):
    """Модель события."""

    template_id: UUID | None = None
    event: EventEnum | None = None
    type: TypeEnum = TypeEnum.email
    users: conlist(UUID, min_items=1)
    data: dict

    @validator('event', always=True)
    def validate_event(cls, event, values):
        """Проверка корректности поля event."""
        if not values.get('template_id') and not event:
            raise HTTPException(status_code=400, detail='Must be one of the fields template_id or event')
        return event


class Notification(Event):
    """Модель уведомления."""

    notification_id: UUID = Field(default_factory=uuid4)
    status: str | None = None


class ScheduledNotification(BaseModel):
    """Модель отложенного уведомления."""

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
    def validate_cron(cls, cron, values):
        """Проверка корректности поля cron."""
        if not values.get('timestamp_start') and not cron:
            raise HTTPException(status_code=400, detail='Must be one of the fields timestamp_start or cron')

        if cron:
            try:
                CronValidator.parse(cron)
            except ValueError as err:
                raise HTTPException(status_code=400, detail='Invalid field cron: {0}'.format(err))

        return cron
