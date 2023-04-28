"""Модели пользовательских данных."""

from uuid import UUID

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """Модель данных пользователя."""

    user_id: UUID
    name: str
    email: EmailStr
    timezone: str
