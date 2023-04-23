from abc import ABC, abstractmethod
from uuid import UUID


class AuthError(Exception):
    """Базовое исключение для ошибок."""


class Auth(ABC):
    @abstractmethod
    async def get(self, user_id: UUID) -> dict:
        """Данные пользователя из Auth сервиса."""
