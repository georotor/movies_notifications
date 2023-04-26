from abc import ABC, abstractmethod
from uuid import UUID


class DBManager(ABC):
    @abstractmethod
    async def find(self, table: str, query: dict):
        """Поиск документов в таблице."""

    @abstractmethod
    async def get_one(self, table: str, query: dict):
        """Выборка одного документа из БД."""

    async def insert_one(self, table: str, obj_data: dict):
        """Создание записи в БД."""

    async def update_one(self, table: str, query: dict, doc: dict):
        """Обновление одного документа в БД."""

    async def get_template_by_id(self, template_id: str) -> dict:
        pass

    @abstractmethod
    async def get_template_by_event_type(self, event: str, type: str) -> dict:
        pass

    @abstractmethod
    async def set_notifications_status(self, notification_id: UUID, status: str):
        pass
