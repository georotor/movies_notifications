from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class Scheduler(ABC):
    @abstractmethod
    async def add(self, task_id: UUID, run_date: datetime, args: tuple):
        """Добавление нотификации в планировщик."""

    @abstractmethod
    async def remove(self, task_id: UUID):
        """Удаление нотификации из планировщика."""
