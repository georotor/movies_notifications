import logging

from fastapi import APIRouter, Depends, status

from models.schemas import Event
from services.notifications import Notifications, get_notification_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    '/',
    summary='Добавить уведомление',
    description='Добавляет уведомление в очередь на отправку.',
    status_code=status.HTTP_201_CREATED,
)
async def notification_create(
        event: Event,
        notifications: Notifications = Depends(get_notification_service)
):
    await notifications.send(event)

    return {'status': 'successfully created'}
