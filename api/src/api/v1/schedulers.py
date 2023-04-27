import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.v1.schemas.schedulers import ScheduledNotificationShort, ScheduledNotificationFull
from db.managers.abstract import AbstractDBManager
from db.managers.mongo import get_db_manager
from models.notifications import ScheduledNotification
from services.notifications import Notifications, NotificationError, get_notification_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    '/',
    summary='Список отложенных уведомлений',
    description='Возвращает список отложенных уведомлений.',
    response_model=list[ScheduledNotificationShort]
)
async def get_list(
    skip: int = 0,
    limit: int = 10,
    db: AbstractDBManager = Depends(get_db_manager)
):
    templates = []
    for template in await db.get('scheduled_notifications', {}, skip, limit):
        templates.append(ScheduledNotificationShort.parse_obj(template))
    return templates


@router.post(
    '/',
    summary='Создать отложенную рассылку',
    description='Создаёт и ставит в очередь на обработку отложенную рассылку.',
    status_code=status.HTTP_201_CREATED,
    response_model=ScheduledNotificationFull
)
async def create(
        notify: ScheduledNotificationFull,
        notifications: Notifications = Depends(get_notification_service)
):
    try:
        result = await notifications.create(ScheduledNotification.parse_obj(notify.dict()))
        return ScheduledNotificationFull.parse_obj(result.dict())
    except NotificationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    '/{scheduled_id}',
    summary='Отложенная рассылка',
    description='Возвращает детальную информации о отложенной рассылке.',
    response_model=ScheduledNotificationFull
)
async def get_one(
    scheduled_id: UUID,
    db: AbstractDBManager = Depends(get_db_manager)
):
    notify = await db.get_one('scheduled_notifications', {'scheduled_id': scheduled_id})
    if notify:
        return ScheduledNotificationFull.parse_obj(notify)

    logger.info('Scheduled notifications {0} not found'.format(scheduled_id))
    raise HTTPException(status_code=404, detail='Scheduled notifications not found')


@router.put(
    '/',
    summary='Обновить отложенную рассылку',
    description='Обновляет существующую рассылку.'
)
async def update(
    notify: ScheduledNotificationFull,
    notifications: Notifications = Depends(get_notification_service)
):
    try:
        await notifications.update(ScheduledNotification.parse_obj(notify.dict()))
    except NotificationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'status': 'Scheduled notification updated'}


@router.delete(
    '/{scheduled_id}',
    summary='Удалить отложенную рассылку',
    description='Останавливает и удаляет отложенную рассылку.',
)
async def delete(
    scheduled_id: UUID,
    notifications: Notifications = Depends(get_notification_service)
):
    try:
        await notifications.remove(scheduled_id)
    except NotificationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'status': 'Scheduled notification removed'}
