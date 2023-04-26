import logging
from datetime import datetime
from uuid import UUID

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from scheduler.abstract import Scheduler


logger = logging.getLogger(__name__)


class PractixScheduler(Scheduler):
    def __init__(self, task_jod):
        self.tasks = {}
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self._jod = task_jod

    async def add(self, task_id: UUID, run_date: datetime, args: tuple):
        if task_id in self.tasks:
            self.tasks[task_id].remove()

        self.tasks[task_id] = self.scheduler.add_job(
            self._run_job,
            'date',
            run_date=run_date,
            args=(task_id, args)
        )

    async def remove(self, task_id: UUID):
        if task_id in self.tasks:
            self.tasks[task_id].remove()
            del self.tasks[task_id]

    async def _run_job(self, task_id: UUID, args: tuple):
        await self._jod(*args)
        del self.tasks[task_id]
