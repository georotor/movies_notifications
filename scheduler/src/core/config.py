"""Настройки приложения."""

from pydantic import BaseModel, BaseSettings


class Logging(BaseModel):
    """Настройки уровней логирования."""

    level_root: str = 'INFO'
    level_console: str = 'DEBUG'


class Settings(BaseSettings):
    """Настройки приложения."""

    mongo_uri: str = 'mongodb://127.0.0.1:27017/'
    mongo_db: str = 'notifications'

    rabbit_uri: str = 'amqp://guest:guest@127.0.0.1/'
    rabbit_exchange: str = 'notifications'
    rabbit_queue_scheduled: str = 'notifications.scheduled'
    rabbit_queue_remove: str = 'notifications.remove'

    auth_url: str = 'http://127.0.0.1:81/api/v1/user/'
    auth_url_list: str = 'http://127.0.0.1:81/api/v1/user/list'
    auth_authorization: str = ''

    logging: Logging = Logging()

    class Config:
        env_nested_delimiter = '__'


settings = Settings()
