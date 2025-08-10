from fastapi import FastAPI, HTTPException, status
from sqlmodel import select
from app.crud.company_research import create_company_research, get_company_research_by_name
from app.models.research import UserCompanyResearch
from app.schemas.user_company_research import UserCompanyResearchCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def get_or_create_company_research(
    session: AsyncSession, user_id: int, data: UserCompanyResearchCreate
) -> UserCompanyResearch:
    existing = await get_company_research_by_name(session, user_id, data.company_name)
    if existing:
        return existing
    return await create_company_research(session, user_id, data)


async def update_company_research(
    research_id: int,
    update_data: UserCompanyResearchCreate,
    user_id: int,
    session: AsyncSession
) -> UserCompanyResearch:
    statement = select(UserCompanyResearch).where(UserCompanyResearch.id == research_id)
    result = await session.execute(statement)
    research = result.scalar_one_or_none()

    if not research:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company research not found")

    if research.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this research")

    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(research, key, value)

    session.add(research)
    await session.commit()
    await session.refresh(research)
    return research