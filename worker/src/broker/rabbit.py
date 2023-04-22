import aio_pika

from broker.abstract import Broker


class Rabbit(Broker):
    def __init__(self, rabbitmq_uri):
        self.rabbitmq_uri = rabbitmq_uri

    async def connect(self):
        return await aio_pika.connect_robust(self.rabbitmq_uri)

    async def create_channel(self):
        connection = await self.connect()
        return await connection.channel()

    async def get_queue(self, queue_name):
        channel = await self.create_channel()
        return await channel.get_queue(queue_name)

    async def consume(self, queue, callback):
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await callback(message)
