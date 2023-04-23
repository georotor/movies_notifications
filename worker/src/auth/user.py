import logging
from uuid import UUID

import aiohttp
import backoff

from auth.abstract import Auth, AuthError

logger = logging.getLogger(__name__)


class UserData(Auth):
    def __init__(self, url: str):
        self.url = url

    @backoff.on_exception(backoff.expo, (AuthError, aiohttp.ClientError))
    async def get(self, user_id: UUID) -> dict | None:
        async with aiohttp.ClientSession() as session:
            async with session.get('{0}/{1}'.format(self.url, user_id)) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    logger.warning('User {0} not found'.format(user_id))
                else:
                    logger.error('Unexpected response status {0}'.format(response.status))
                    raise AuthError('Unexpected response status: {0}'.format(response.status))

                return None