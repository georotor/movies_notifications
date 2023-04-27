import logging

from fastapi import APIRouter, Depends, status

from models.notifications import Event
from services.notifications import Notifications, get_notification_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    '/',
    summary='Добавить неотложное уведомление',
    description='Добавляет неотложное уведомление в очередь на отправку.',
    status_code=status.HTTP_201_CREATED,
)
async def notification_create(
        event: Event,
        notifications: Notifications = Depends(get_notification_service)
):
    print(1)
    await notifications.send(event)

    return {'status': 'successfully created'}
