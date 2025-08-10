from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.utils.email_schedular import check_pending_applications

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(
        check_pending_applications,
        CronTrigger(hour=9, minute=0),  
    )
    scheduler.start()
