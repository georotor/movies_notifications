from pydantic import BaseModel

from models.schemas import EventEnum, TypeEnum


class TemplateShort(BaseModel):
    template_id: str
    name: str
    event: EventEnum | None
    type: TypeEnum


class TemplateFull(TemplateShort):
    subject: str | None
    content: str
