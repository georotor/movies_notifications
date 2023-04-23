from abc import ABC, abstractmethod
from uuid import UUID


class DBManager(ABC):
    @abstractmethod
    async def get_template_by_id(self, template_id: str) -> dict:
        pass

    @abstractmethod
    async def get_template_by_event_type(self, event: str, type: str) -> dict:
        pass

    @abstractmethod
    async def set_notifications_status(self, notification_id: UUID, status: str):
        pass
