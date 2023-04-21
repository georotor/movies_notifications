from aio_pika import RobustConnection

rabbit: RobustConnection | None = None


async def get_rabbit() -> RobustConnection:
    return rabbit
