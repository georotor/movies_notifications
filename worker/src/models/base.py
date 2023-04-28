"""Базовые модели."""

from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class BrokerMessage(BaseModel):
    """Модель сообщения брокера."""

    notification_id: UUID


class EventEnum(str, Enum):
    """Список доступных событий."""

    registered = 'registered'


class TypeEnum(str, Enum):
    """Список доступных видов уведомлений."""

    email = 'email'
