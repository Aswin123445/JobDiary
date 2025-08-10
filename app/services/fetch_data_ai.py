from select import select
from sqlalchemy.orm import selectinload
from app.models.research import JobApplication, UserJobResearch
from sqlmodel.ext.asyncio.session import AsyncSession

async def get_application_research(application_id: int, session: AsyncSession):
    stmt = (
        select(JobApplication)
        .where(JobApplication.id == application_id)
        .options(
            selectinload(JobApplication.job_research)
            .selectinload(UserJobResearch.company_research)
        )
    )
    res = await session.exec(stmt)
    return res.scalar_one_or_none()
