"""Реализация AbstractBrokerManager для RabbitMQ."""
import logging

from aio_pika import Message, RobustConnection
from fastapi import Depends

from db.managers.abstract import AbstractBrokerManager
from db.rabbit import get_rabbit
from models.schemas import Notification

logger = logging.getLogger(__name__)


class RabbitManager(AbstractBrokerManager):
    """Реализация AbstractBrokerManager для Rabbit."""

    def __init__(self, rabbit):
        """Конструктор класса.

        :param rabbit: Инициированное подключение к брокеру
        """
        self.rabbit = rabbit
        self.channel = None
        self.exchange = None

    async def init_async(self):
        """Асинхронная инициализация обменника в брокере."""
        self.channel = await self.rabbit.channel()
        self.exchange = await self.channel.declare_exchange('direct', auto_delete=True, durable=True)

    async def publish(self, msg: Notification):
        """Публикация сообщения в брокере.

        :param msg: Сообщение для публикации
        """
        queue = await self.channel.declare_queue(name=msg.event, auto_delete=True, durable=True)
        await queue.bind(self.exchange, msg.event)

        await self.exchange.publish(
            Message(body=msg.json().encode()),
            routing_key=msg.event
        )


async def get_broker_manager(rabbit: RobustConnection = Depends(get_rabbit)) -> AbstractBrokerManager:
    """DI для FastAPI. Получаем менеджер для Rabbit."""
    manager = RabbitManager(rabbit=rabbit)
    await manager.init_async()
    return manager
