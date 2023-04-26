import json
from typing import Type

import aio_pika
from pydantic import BaseModel

from broker.abstract import Broker


class Rabbit(Broker):
    def __init__(self, rabbitmq_uri: str):
        self.rabbitmq_uri = rabbitmq_uri
        self.exchange = None
        self.connection = None
        self.chanel = None

    async def connect(self):
        if self.connection is None:
            self.connection = await aio_pika.connect_robust(self.rabbitmq_uri)
        return self.connection

    async def _create_channel(self):
        connection = await self.connect()
        if self.chanel is None:
            self.chanel = await connection.channel()
        return self.chanel

    async def _create_exchange(self, exchange):
        if self.exchange is None:
            channel = await self._create_channel()
            self.exchange = await channel.get_exchange(exchange)
        return self.exchange

    async def _get_queue(self, queue_name: str):
        channel = await self._create_channel()
        return await channel.get_queue(queue_name)

    async def consume(self, queue_name, callback):
        queue = await self._get_queue(queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                context = json.loads(message.body.decode())
                # TODO: Нужен контроль исключений
                await callback(context)
                await message.ack()

    async def publish(self, exchange_name: str, msg: Type[BaseModel], routing_key: str):
        """Публикация сообщения в брокере."""
        exchange = await self._create_exchange(exchange_name)
        await exchange.publish(
            aio_pika.Message(body=msg.json().encode()),
            routing_key=routing_key
        )
