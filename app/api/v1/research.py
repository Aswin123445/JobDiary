from zipfile import Path
from fastapi import APIRouter, Depends, status
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user_company_research import UserCompanyResearchCreate, UserCompanyResearchRead
from app.services.company_research import get_or_create_company_research, update_company_research
from app.utils.get_current_user import get_current_user
from app.db.session import get_db
router = APIRouter(prefix="/company-research", tags=["company_research"])


@router.post("/", response_model=UserCompanyResearchRead, status_code=status.HTTP_201_CREATED)
async def create_company_research(
    company_research_in: UserCompanyResearchCreate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    company_research = await get_or_create_company_research(
        session=session,
        user_id=current_user.id,
        data=company_research_in
    )
    return company_research

@router.patch("/company-research/{research_id}", response_model=UserCompanyResearchRead)
async def patch_company_research(
    *,
    research_id: int ,
    research_update: UserCompanyResearchCreate,
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    updated_research = await update_company_research(
        research_id=research_id,
        update_data=research_update,
        user_id=current_user.id,
        session=session,
    )
    return updated_research




