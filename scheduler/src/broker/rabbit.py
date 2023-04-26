import json
from typing import Type

import aio_pika
from pydantic import BaseModel

from broker.abstract import Broker, BrokerConnectionError


class Rabbit(Broker):
    def __init__(self, rabbitmq_uri: str):
        self.rabbitmq_uri = rabbitmq_uri
        self.exchange = None
        self.connection = None

    async def connect(self):
        if self.connection is None:
            self.connection = await aio_pika.connect_robust(self.rabbitmq_uri)
        return self.connection

    async def create_channel(self):
        connection = await self.connect()
        return await connection.channel()

    async def get_queue(self, queue_name: str):
        channel = await self.create_channel()
        return await channel.get_queue(queue_name)

    async def consume(self, queue, callback):
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                context = json.loads(message.body.decode())
                # TODO: Нужен контроль исключений
                await callback(context)
                await message.ack()

    async def create_exchange(self, exchange):
        if self.exchange is None:
            channel = await self.create_channel()
            self.exchange = await channel.get_exchange(exchange)
        return self.exchange

    async def publish(self, msg: Type[BaseModel], routing_key: str):
        """Публикация сообщения в брокере."""
        await self.exchange.publish(
            aio_pika.Message(body=msg.json().encode()),
            routing_key=routing_key
        )
