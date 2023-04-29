"""Модуль получения данных пользователей."""

import json
import logging
from uuid import UUID
from http import HTTPStatus

import aiohttp
import backoff

from auth.abstract import Auth, AuthError

logger = logging.getLogger(__name__)


class UserData(Auth):
    """Класс получения данных пользователей."""

    def __init__(self, url: str, url_list: str, token: str):
        """Инициализация объекта."""
        self.url = url
        self.url_list = url_list
        self.headers = {'Authorization': token}

    @backoff.on_exception(backoff.expo, (AuthError, aiohttp.ClientError))
    async def get(self, user_id: UUID) -> dict | None:
        """Получения данных одного пользователя."""
        async with aiohttp.ClientSession() as session:
            async with session.get('{0}/{1}'.format(self.url, user_id), headers=self.headers) as response:
                if response.status == HTTPStatus.OK:
                    return await response.json()
                elif response.status == HTTPStatus.NOT_FOUND:
                    logger.warning('User {0} not found'.format(user_id))
                else:
                    logger.error('Unexpected response status {0}'.format(response.status))
                    raise AuthError('Unexpected response status: {0}'.format(response.status))

                return None

    @backoff.on_exception(backoff.expo, (AuthError, aiohttp.ClientError))
    async def get_list(self, user_ids: list[UUID]) -> list | None:
        """Получения данных списка пользователей."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    self.url_list,
                    json=json.dumps(user_ids, default=str),
                    headers=self.headers
            ) as response:
                if response.status == HTTPStatus.OK:
                    return await response.json()
                elif response.status == HTTPStatus.NOT_FOUND:
                    logger.warning('Users not found')
                else:
                    logger.error('Unexpected response status {0}'.format(response.status))
                    raise AuthError('Unexpected response status: {0}'.format(response.status))
