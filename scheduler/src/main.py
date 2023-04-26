import asyncio
from logging import config as logging_config

from auth.user import UserData
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

    scheduler = PractixScheduler(broker.publish, settings.rabbit_exchange)

    notification_message = Message(db, auth, scheduler)
    await notification_message.init()

    await broker.consume(settings.rabbit_queue_scheduled, notification_message.incoming)
    await broker.consume(settings.rabbit_queue_remove, notification_message.remove)

    try:
        await asyncio.Future()
    finally:
        await broker.connection.close()

if __name__ == "__main__":
    asyncio.run(main())
