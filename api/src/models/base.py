"""Базовые модели."""

from uuid import UUID

from pydantic import BaseModel


class BrokerMessage(BaseModel):
    """Модель сообщений брокера."""

    notification_id: UUID
