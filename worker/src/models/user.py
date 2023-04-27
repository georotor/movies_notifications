from uuid import UUID
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: UUID
    name: str
    email: EmailStr
    timezone: str
