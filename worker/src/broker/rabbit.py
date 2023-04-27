import logging
import json
from typing import Any, Callable

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

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