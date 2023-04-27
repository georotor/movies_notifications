from abc import ABC, abstractmethod
from uuid import UUID


class AuthError(Exception):
    """Базовое исключение для ошибок."""


class Auth(ABC):
    @abstractmethod
    async def get(self, user_id: UUID) -> dict:
        """Данные пользователя из Auth сервиса."""

    @abstractmethod
    async def get_list(self, user_ids: list[UUID]) -> list | None:
        """Данные пользователей из Auth сервиса."""
