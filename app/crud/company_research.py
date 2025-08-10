from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.research import UserCompanyResearch
from app.schemas.user_company_research import UserCompanyResearchCreate
async def get_company_research_by_name(
    session: AsyncSession, user_id: int, company_name: str
) -> Optional[UserCompanyResearch]:
    statement = select(UserCompanyResearch).where(
        UserCompanyResearch.user_id == user_id,
        UserCompanyResearch.company_name == company_name
    )
    result = await session.execute(statement)  
    return result.scalars().first()


async def create_company_research(
    session: AsyncSession, user_id: int, data: UserCompanyResearchCreate
) -> UserCompanyResearch:
    company_research = UserCompanyResearch(user_id=user_id, **data.model_dump())
    session.add(company_research)
    await session.commit()
    await session.refresh(company_research)
    return company_research