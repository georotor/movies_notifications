"""Модуль для управления уведомлениями в хранилище."""

from abc import ABC, abstractmethod
from uuid import UUID


class DBManager(ABC):
    """Класс для управления уведомлениями в хранилище."""

    @abstractmethod
    async def get_template_by_id(self, template_id: UUID) -> dict | None:
        """Поиск шаблона по его id."""

    @abstractmethod
    async def get_template_by_event_type(self, event: str, notify_type: str) -> dict:
        """Поиск шаблона по типу события и типу уведомления."""

    @abstractmethod
    async def get_notification_by_id(self, notification_id: UUID) -> dict | None:
        """Поиск актуального, включенного и не выполненного уведомления."""

    @abstractmethod
    async def set_notifications_status(self, notification_id: UUID, status: str):
        """Установка статуса и времени последнего обновления для уведомления."""
