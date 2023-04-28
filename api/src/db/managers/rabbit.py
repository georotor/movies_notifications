"""Реализация AbstractBrokerManager для RabbitMQ."""
import logging

from aio_pika import Message, RobustConnection
from fastapi import Depends
from pydantic import BaseModel

from core.config import settings
from db.managers.abstract import AbstractBrokerManager
from db.rabbit import get_rabbit

logger = logging.getLogger(__name__)


class RabbitManager(AbstractBrokerManager):
    """Реализация AbstractBrokerManager для Rabbit."""

    def __init__(self, rabbit, exchange_name):
        """Конструктор класса."""
        self.rabbit = rabbit
        self.channel = None
        self.exchange = None
        self.exchange_name = exchange_name

    async def init_async(self):
        """Асинхронная инициализация обменника в брокере."""
        self.channel = await self.rabbit.channel()
        self.exchange = await self.channel.get_exchange(self.exchange_name)

    async def publish(self, msg: BaseModel, routing_key: str, priority: int | None = None):
        """Публикация сообщения в брокере."""
        await self.exchange.publish(
            Message(body=msg.json().encode(), priority=priority),
            routing_key=routing_key
        )


async def get_broker_manager(rabbit: RobustConnection = Depends(get_rabbit)) -> AbstractBrokerManager:
    """DI для FastAPI. Получаем менеджер для Rabbit."""
    manager = RabbitManager(rabbit=rabbit, exchange_name=settings.rabbit_exchange)
    await manager.init_async()
    return manager
