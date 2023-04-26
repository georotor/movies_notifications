import logging
from datetime import datetime
from uuid import UUID

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from scheduler.abstract import Scheduler


logger = logging.getLogger(__name__)


class PractixScheduler(Scheduler):
    def __init__(self, task_job, exchange_name):
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self._job = task_job
        self.exchange_name = exchange_name

    async def add(self, task_id: UUID, run_date: datetime, args: tuple):
        """Добавление нотификации в планировщик по дате."""
        if self.scheduler.get_job(job_id=str(task_id)):
            self.scheduler.get_job(job_id=str(task_id)).remove()

        return self.scheduler.add_job(
            self._job,
            'date',
            run_date=run_date,
            args=(self.exchange_name,) + args,
            id=str(task_id)
        )

    async def add_cron(self, task_id: UUID, cron: str, timezone: str, args: tuple):
        """Добавление нотификации в планировщик по крону."""
        if self.scheduler.get_job(job_id=str(task_id)):
            self.scheduler.get_job(job_id=str(task_id)).remove()

        return self.scheduler.add_job(
            self._job,
            CronTrigger.from_crontab(cron, timezone=timezone),
            args=(self.exchange_name,) + args,
            id=str(task_id)
        )

    async def remove(self, task_id: UUID):
        """Удаление нотификации из планировщика."""
        if self.scheduler.get_job(job_id=str(task_id)):
            self.scheduler.get_job(job_id=str(task_id)).remove()
            logger.info('Notification {0} removed from scheduler'.format(task_id))
            return

        logger.warning('Notification {0} not found in scheduler'.format(task_id))
