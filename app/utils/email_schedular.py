from datetime import datetime, timedelta
from sqlalchemy import select
from app.models.research import JobApplication
from app.models.user import User
from app.utils.send_follow_up_mail import send_email
import logging
from app.db.session import async_session
logger = logging.getLogger(__name__)

async def check_pending_applications():
    ten_days_ago = datetime.utcnow() - timedelta(seconds=3)
    async with async_session() as session:
        stmt = (
            select(JobApplication, User)
            .join(User, JobApplication.user_id == User.id)
            .where(
                JobApplication.status == "pending",
                JobApplication.application_date < ten_days_ago,
                JobApplication.last_reminder_sent.is_(None)  # prevents duplicates
            )
        )

        res = await session.execute(stmt)
        results = res.all()

        for app, user in results:
            await send_email(
                to=user.email,
                subject="Follow-up reminder for your job application",
                body=f"Hi {user.name},\n\nIt's been over 10 days since you applied to job ID {app.id}. Consider sending a follow-up email."
            )
            app.last_reminder_sent = datetime.utcnow()
            logger.info(f"Reminder sent to {user.email} for application {app.id}")
        await session.commit()
