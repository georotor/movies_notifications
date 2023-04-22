from abc import ABC, abstractmethod


class DBManager(ABC):
    @abstractmethod
    async def get_template(self, template_id: str) -> dict:
        pass
