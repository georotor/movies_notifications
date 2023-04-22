from pydantic import BaseModel, BaseSettings


class Logging(BaseModel):
    level_root: str = 'INFO'
    level_uvicorn: str = 'INFO'
    level_console: str = 'DEBUG'


class Settings(BaseSettings):

    mongo_uri: str = 'mongodb://127.0.0.1:27017/'
    mongo_db: str = 'notifications'
    rabbit_uri: str = 'amqp://guest:guest@127.0.0.1/'
    rabbit_queue: str = 'emails.send'

    sendgrid_api_key: str = ''
    sendgrid_from_email: str = ''

    logging: Logging = Logging()

    class Config:
        env_nested_delimiter = '__'


settings = Settings()
