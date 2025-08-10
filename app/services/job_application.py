from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status
from datetime import datetime

from app.models.research import JobApplication, UserJobResearch
from app.schemas.job_application import JobApplicationCreate
from app.utils.make_native import make_naive

from sqlalchemy.orm import selectinload

async def create_job_application(
    data: JobApplicationCreate,
    user_id: int,
    session: AsyncSession,
) -> JobApplication:
    # Verify the job research exists
    stmt = select(UserJobResearch).where(UserJobResearch.id == data.job_research_id)
    res = await session.execute(stmt)
    job_research = res.scalar_one_or_none()

    if not job_research:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job research not found")

    # Check if this user already has an application for this job research
    existing_stmt = select(JobApplication).where(
        and_(
            JobApplication.user_id == user_id,
            JobApplication.job_research_id == data.job_research_id,
        )
    )
    existing_res = await session.execute(existing_stmt)
    existing_application = existing_res.scalars().first()
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job application already exists for this job research"
        )

    application_date = make_naive(data.application_date or datetime.utcnow())
    resume_url = data.resume_url
    if resume_url:
        resume_url = str(resume_url)  # convert HttpUrl to str

    job_application = JobApplication(
        user_id=user_id,
        job_research_id=data.job_research_id,
        application_date=application_date,
        resume_url=resume_url,
        status=data.status,
        notes=data.notes,
    )
    session.add(job_application)
    await session.commit()
    await session.refresh(job_application)
    return job_application

async def delete_job_application(application_id: int, user_id: int, session: AsyncSession):
    stmt = select(JobApplication).options(
        selectinload(JobApplication.job_research).selectinload(UserJobResearch.company_research)
    ).where(JobApplication.id == application_id)

    res = await session.execute(stmt)
    application = res.scalar_one_or_none()

    if not application:
        raise HTTPException(404, "Application not found")

    if application.user_id != user_id:
        raise HTTPException(403, "Not authorized")

    # Get related job research and company research ids
    job_research = application.job_research
    company_research = job_research.company_research if job_research else None

    # Delete the application
    await session.delete(application)
    await session.commit()

    # Check if job research has any other applications
    stmt = select(JobApplication).where(JobApplication.job_research_id == job_research.id)
    res = await session.execute(stmt)
    other_apps = res.scalars().first()

    if not other_apps:
        # No other applications - delete job research
        await session.delete(job_research)
        await session.commit()

        # Check if company research has other job researches
        stmt = select(UserJobResearch).where(UserJobResearch.company_research_id == company_research.id)
        res = await session.execute(stmt)
        other_jobs = res.scalars().first()

        if not other_jobs:
            # No other jobs - delete company research
            await session.delete(company_research)
            await session.commit()

    return