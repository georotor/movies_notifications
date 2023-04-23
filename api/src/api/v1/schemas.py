from pydantic import BaseModel, Field

from models.schemas import EventEnum, TypeEnum


class TemplateShort(BaseModel):
    template_id: str
    name: str
    event: EventEnum | None
    type: TypeEnum


class TemplateFull(TemplateShort):
    content: str
