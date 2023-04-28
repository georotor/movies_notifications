"""DI для базы подключения к Rabbit."""

from aio_pika import RobustConnection

rabbit: RobustConnection | None = None


async def get_rabbit() -> RobustConnection:
    """DI для базы подключения к Rabbit."""
    return rabbit
