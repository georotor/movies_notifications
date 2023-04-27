import logging
import json
from typing import Any, Callable, Type

import aio_pika
import backoff
from aio_pika.abc import AbstractIncomingMessage
from aiormq.exceptions import ChannelInvalidStateError
from pydantic import BaseModel

from broker.abstract import Broker

logger = logging.getLogger(__name__)


class Rabbit(Broker):
    def __init__(self, rabbitmq_uri: str):
        self.rabbitmq_uri = rabbitmq_uri
        self.exchange = None
        self.connection = None
        self.chanel = None

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def _connect(self) -> aio_pika.abc.AbstractRobustConnection:
        if self.connection is None:
            self.connection = await aio_pika.connect_robust(self.rabbitmq_uri)
        return self.connection

    async def _create_channel(self) -> aio_pika.abc.AbstractChannel:
        connection = await self._connect()
        if self.chanel is None:
            self.chanel = await connection.channel()
        return self.chanel

    async def _get_queue(self, queue_name: str) -> aio_pika.abc.AbstractQueue:
        channel = await self._create_channel()
        return await channel.get_queue(queue_name)

    async def consume(self, queue_name: str, callback: Callable[[dict], Any]):
        queue = await self._get_queue(queue_name)

        async def on_message(message: AbstractIncomingMessage):
            try:
                context = json.loads(message.body.decode())
                logger.info('Consume message {0} from queue {1}'.format(context, queue_name))
                await callback(context)
            except json.decoder.JSONDecodeError as e:
                logger.error('Invalid json in message body: {0}'.format(e))

            await message.ack()

        await queue.consume(on_message)

    async def _create_exchange(self, exchange) -> aio_pika.abc.AbstractExchange:
        if self.exchange is None:
            channel = await self._create_channel()
            self.exchange = await channel.get_exchange(exchange)
        return self.exchange

    @backoff.on_exception(backoff.expo, ChannelInvalidStateError)
    async def publish(self, exchange_name: str, msg: Type[BaseModel], routing_key: str):
        """Публикация сообщения в брокере."""
        exchange = await self._create_exchange(exchange_name)
        await exchange.publish(
            aio_pika.Message(body=msg.json().encode()),
            routing_key=routing_key
        )
