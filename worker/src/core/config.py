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

    auth_url: str = 'http://127.0.0.1/api/v1/user/'

    sendgrid_api_key: str = ''
    sendgrid_from_email: str = ''

    mailgun_api_key: str = 'ca09f6a54bc3f6750e51c506a2cbfbc9-181449aa-40c3080b'
    mailgun_domain: str = 'sandbox615c3c759bdf40ffae68cf5fccf6747f.mailgun.org'
    mailgun_from_email: str = 'Excited User <mailgun@sandbox615c3c759bdf40ffae68cf5fccf6747f.mailgun.org>'

    logging: Logging = Logging()

    class Config:
        env_nested_delimiter = '__'


settings = Settings()
