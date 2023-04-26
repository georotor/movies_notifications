from uuid import UUID

from pydantic import BaseModel


class BrokerMessage(BaseModel):
    notification_id: UUID
