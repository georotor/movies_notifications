"""API управления шаблонами для уведомлений."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.v1.schemas.templates import TemplateShort, TemplateFull
from db.managers.abstract import AbstractDBManager
from db.managers.mongo import get_db_manager
from models.templates import Template


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    '/',
    summary='Создать шаблон',
    description='Создает шаблон, используемый для отправки уведомлений.',
    status_code=status.HTTP_201_CREATED,
)
async def create(
        template: Template,
        db: AbstractDBManager = Depends(get_db_manager)
):
    """Создание шаблона."""
    if template.event is not None:
        result = await db.get_one('templates', {'event': template.event, 'type': template.type})
        if result:
            raise HTTPException(status_code=400, detail='Template with this event and type already exists')

    result = await db.save('templates', template.dict())

    logger.info('Created template {0} {1}'.format(result.inserted_id, template))
    return {
        'status': 'successfully created',
        'template_id': template.template_id,
    }


@router.get(
    '/',
    summary='Список шаблонов',
    description='Возвращает список сохраненных шаблонов.',
    response_model=list[TemplateShort]
)
async def get_list(
    skip: int = 0,
    limit: int = 10,
    db: AbstractDBManager = Depends(get_db_manager)
):
    """Список шаблонов."""
    templates = []
    for template in await db.get('templates', {}, skip, limit):
        templates.append(TemplateShort.parse_obj(template))
    return templates


@router.get(
    '/{template_id}',
    summary='Шаблон',
    description='Возвращает детальную информации о шаблоне.',
    response_model=TemplateFull
)
async def get_one(
    template_id: UUID,
    db: AbstractDBManager = Depends(get_db_manager)
):
    """Получение шаблона."""
    template = await db.get_one('templates', {'template_id': template_id})
    if template:
        return TemplateFull.parse_obj(template)

    logger.info('Template {0} not found'.format(template_id))
    raise HTTPException(status_code=404, detail='Template not found')


@router.put(
    '/',
    summary='Обновить шаблон',
    description='Обновляет существующий шаблон.',
    response_model=TemplateFull
)
async def update(
    template: Template,
    db: AbstractDBManager = Depends(get_db_manager)
):
    """Обновление шаблона."""
    template_id = template.template_id
    result = await db.update_one(
        'templates',
        {'template_id': template_id},
        template.dict(exclude={'template_id': True})
    )

    if result.modified_count == 1:
        logger.info('Template {0} updated'.format(template_id))
        return TemplateFull.parse_obj(await db.get_one('templates', {'template_id': template_id}))

    logger.info('Template {0} not found'.format(template_id))
    raise HTTPException(status_code=404, detail='Template not found')


@router.delete(
    '/{template_id}',
    summary='Удалить шаблон',
    description='Удаляет существующий шаблон.',
)
async def delete(
    template_id: UUID,
    db: AbstractDBManager = Depends(get_db_manager)
):
    """Удаление шаблона."""
    result = await db.delete_one('templates', {'template_id': template_id})

    if result.deleted_count == 1:
        logger.info('Template {0} deleted'.format(template_id))
        return {'message': 'Template deleted'}

    logger.info('Template {0} not found'.format(template_id))
    raise HTTPException(status_code=404, detail='Template not found')
