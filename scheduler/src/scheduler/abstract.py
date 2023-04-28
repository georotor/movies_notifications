"""Модуль планировщика отложенных уведомлений."""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class Scheduler(ABC):
    """Класс планировщика отложенных уведомлений."""

    @abstractmethod
    async def add(self, task_id: UUID, run_date: datetime, args: tuple):
        """Добавление нотификации в планировщик по дате."""

    @abstractmethod
    async def add_cron(self, task_id: UUID, cron: str, timezone: str, args: tuple):
        """Добавление нотификации в планировщик по крону."""

    @abstractmethod
    async def remove(self, task_id: UUID):
        """Удаление нотификации из планировщика."""
