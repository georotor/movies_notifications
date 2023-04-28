"""Модели данных."""

from enum import Enum
from uuid import UUID, uuid4
from typing import Optional

from cron_validator import CronValidator
from pydantic import BaseModel, Field, validator


class EventEnum(str, Enum):
    """Список событий для уведомлений."""

    registered = 'registered'


class TypeEnum(str, Enum):
    """Список видов уведомлений."""

    email = 'email'


class BaseNotification(BaseModel):
    """Базовая модель уведомлений."""

    template_id: UUID | None
    event: EventEnum | None
    type: TypeEnum = TypeEnum.email
    users: list[UUID]
    data: dict


class ScheduledNotification(BaseNotification):
    """Модель отложенного уведомления."""

    scheduled_id: UUID = Field(default_factory=uuid4)
    sub_notifications: Optional[list[tuple[UUID, str]]] = []
    timestamp_start: int | None
    cron: str | None
    enabled: bool = True

    @validator('cron', always=True)
    def validate_subject(cls, cron, values):
        """Проверка поля cron."""
        if not values.get('timestamp_start') and not cron:
            raise ValueError('Must be one of the fields timestamp_start or cron')

        if cron:
            try:
                CronValidator.parse(cron)
            except ValueError as err:
                raise ValueError('Invalid field cron {0}: {1}'.format(cron, err))

        return cron


class SubScheduledNotification(BaseNotification):
    """Модель неотложного уведомления."""

    notification_id: UUID = Field(default_factory=uuid4)
    scheduled_id: UUID
    status: str | None = None


class BrokerMessage(BaseModel):
    """Модель сообщения брокера."""

    notification_id: UUID
