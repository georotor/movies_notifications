from db.abstract import DBManager

from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBManager(DBManager):
    def __init__(self, uri: str, database_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.database = self.client[database_name]
        self.templates = self.database['templates']

    async def get_template(self, template_id: str) -> dict:
        template = await self.templates.find_one({"_id": template_id})
        return template
