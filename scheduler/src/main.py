import asyncio
from logging import config as logging_config

import backoff

from auth.user import UserData
from broker.abstract import BrokerConnectionError
from broker.rabbit import Rabbit
from db.mongo import MongoDBManager
from core.config import settings
from core.logger import LOGGING
from notification.message import Message
from scheduler.scheduler import PractixScheduler

logging_config.dictConfig(LOGGING)


async def main():
    broker = Rabbit(settings.rabbit_uri)
    db = MongoDBManager(settings.mongo_uri, settings.mongo_db)
    auth = UserData(settings.auth_url, settings.auth_url_list)

    scheduler = PractixScheduler(broker.publish)
    notification_message = Message(db, auth, scheduler)

    scheduled_queue = await broker.get_queue(settings.rabbit_queue_scheduled)
    remove_queue = await broker.get_queue(settings.rabbit_queue_remove)

    await broker.create_exchange(settings.rabbit_exchange)

    await broker.consume(scheduled_queue, notification_message.scheduled)
    await broker.consume(remove_queue, notification_message.remove)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
