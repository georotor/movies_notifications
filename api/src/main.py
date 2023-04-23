from logging import config as logging_config

import backoff
import uvicorn
from aio_pika import connect_robust
from aio_pika.exceptions import AMQPException
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import events, templates
from db import mongo, rabbit
from core.config import settings
from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
@backoff.on_exception(backoff.expo, (AMQPException,))
async def startup():
    """Поднимаем RabbitMQ и Mongo при запуске API."""
    mongo.mongo = AsyncIOMotorClient(
        settings.mongo_uri,
        uuidRepresentation='standard'
    )
    rabbit.rabbit = await connect_robust(settings.rabbit_uri)


@app.on_event('shutdown')
async def shutdown():
    """Закрываем подключения к БД при выключении API."""
    mongo.mongo.close()
    await rabbit.rabbit.close()


app.include_router(events.router, prefix='/api/v1/notifications', tags=['notifications'])
app.include_router(templates.router, prefix='/api/v1/templates', tags=['templates'])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
