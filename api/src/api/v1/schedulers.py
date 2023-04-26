import logging

from fastapi import APIRouter, Depends, HTTPException, status

from models.schemas import ScheduledNotification
from services.notifications import Notifications, NotificationError, get_notification_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    '/',
    summary='Создать отложенную рассылку',
    description='Ставит в очередь на обработку отложенную рассылку.',
    status_code=status.HTTP_201_CREATED,
)
async def create(
        event: ScheduledNotification,
        notifications: Notifications = Depends(get_notification_service)
):
    try:
        await notifications.scheduled(event)
        return {'status': 'Queued for processing'}
    except NotificationError as e:
        raise HTTPException(status_code=400, detail=str(e))
