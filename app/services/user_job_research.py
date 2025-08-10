from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from app.models.research import UserCompanyResearch, UserJobResearch
from app.schemas.user_job_research import UserJobResearchCreate, UserJobResearchUpdate

async def create_job_research(
    data: UserJobResearchCreate,
    user_id: int,
    session: AsyncSession
) -> UserJobResearch:
    # Verify company_research exists and belongs to user
    stmt = select(UserCompanyResearch).where(UserCompanyResearch.id == data.company_research_id)
    res = await session.execute(stmt)
    company_research = res.scalar_one_or_none()
    if not company_research:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company research not found")
    if company_research.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this company research")

    job_research = UserJobResearch(**data.dict())
    session.add(job_research)
    await session.commit()
    await session.refresh(job_research)
    return job_research


async def update_job_research(
    research_id: int,
    update_data: UserJobResearchUpdate,
    user_id: int,
    session: AsyncSession
) -> UserJobResearch:
    stmt = select(UserJobResearch).where(UserJobResearch.id == research_id)
    res = await session.execute(stmt)
    job_research = res.scalar_one_or_none()

    if not job_research:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job research not found")

    # Check ownership via company research
    stmt2 = select(UserCompanyResearch).where(UserCompanyResearch.id == job_research.company_research_id)
    res2 = await session.execute(stmt2)
    company_research = res2.scalar_one_or_none()
    if not company_research or company_research.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this job research")

    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(job_research, key, value)

    session.add(job_research)
    await session.commit()
    await session.refresh(job_research)
    return job_research
