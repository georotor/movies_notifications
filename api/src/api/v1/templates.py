import logging

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from db.managers.abstract import AbstractDBManager
from db.managers.mongo import get_db_manager
from models.schemas import Template
from .schemas import TemplateShort, TemplateFull


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
    if template.event is not None:
        result = await db.get_one('templates', {'event': template.event, 'type': template.type})
        if result:
            raise HTTPException(status_code=400, detail='Template with this event and type already exists')

    result = await db.save('templates', template.dict())

    logger.info('Created template {0} {1}'.format(result.inserted_id, template))
    return {
        'status': 'successfully created',
        'template_id': str(result.inserted_id),
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
    templates = []
    for template in await db.get('templates', {}, skip, limit):
        templates.append(TemplateShort.parse_obj({
            **template,
            'template_id': str(template['_id'])
        }))
    return templates


@router.get(
    '/{template_id}',
    summary='Шаблон',
    description='Возвращает детальную информации о шаблоне.',
    response_model=TemplateFull
)
async def get_one(
    template_id: str,
    db: AbstractDBManager = Depends(get_db_manager)
):
    template = await db.get_one('templates', {'_id': ObjectId(template_id)})
    if template:
        return TemplateFull.parse_obj({
            **template,
            'template_id': str(template['_id'])
        })

    logger.info('Template {0} not found'.format(template_id))
    raise HTTPException(status_code=404, detail='Template not found')


@router.put(
    '/{template_id}',
    summary='Обновить шаблон',
    description='Обновляет существующий шаблон.',
    response_model=TemplateFull
)
async def update(
    template_id: str,
    template: Template,
    db: AbstractDBManager = Depends(get_db_manager)
):
    result = await db.update_one('templates', template_id, template.dict())

    if result.modified_count == 1:
        logger.info('Template {0} updated'.format(template_id))
        return TemplateFull.parse_obj({
            **template.dict(),
            'template_id': template_id
        })

    logger.info('Template {0} not found'.format(template_id))
    raise HTTPException(status_code=404, detail='Template not found')


@router.delete(
    '/{template_id}',
    summary='Удалить шаблон',
    description='Удаляет существующий шаблон.',
)
async def delete(
    template_id: str,
    db: AbstractDBManager = Depends(get_db_manager)
):
    result = await db.delete_one('templates', template_id)

    if result.deleted_count == 1:
        logger.info('Template {0} deleted'.format(template_id))
        return {'message': 'Template deleted'}

    logger.info('Template {0} not found'.format(template_id))
    raise HTTPException(status_code=404, detail='Template not found')
