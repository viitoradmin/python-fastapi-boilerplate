import asyncio

import constant
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from scheduler_job import ScheduerJob

app = FastAPI()
scheduler = BackgroundScheduler()


async def schedule_job():
    # Add schedulers to background for inactive/delete the past event
    scheduler.add_job(
        ScheduerJob().delete_past_events,
        CronTrigger(
            day_of_week="mon-sun",
            hour=constant.STATUS_ONE,
            minute=constant.THIRTY,
            timezone="Asia/Kolkata",
        ),
    )
    scheduler.start()


asyncio.run(schedule_job())