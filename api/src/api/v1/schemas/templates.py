from uuid import UUID
from pydantic import BaseModel


from models.notifications import EventEnum, TypeEnum


class TemplateShort(BaseModel):
    template_id: UUID
    name: str
    event: EventEnum | None
    type: TypeEnum


class TemplateFull(TemplateShort):
    subject: str | None
    content: str
