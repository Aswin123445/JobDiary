
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user_job_research import UserJobResearchCreate, UserJobResearchRead, UserJobResearchUpdate
from app.services.user_job_research import create_job_research, update_job_research
from app.utils.get_current_user import get_current_user
from app.db.session import get_db
router = APIRouter(prefix="/job-research", tags=["job_research"])
@router.post("/", response_model=UserJobResearchRead, status_code=status.HTTP_201_CREATED)
async def create_job_research_endpoint(
    job_research_in: UserJobResearchCreate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    job_research = await create_job_research(
        data=job_research_in,
        user_id=current_user.id,
        session=session,
    )
    return job_research


@router.patch("/{research_id}", response_model=UserJobResearchRead)
async def update_job_research_endpoint(
    *,
    research_id: int ,
    job_research_update: UserJobResearchUpdate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    updated_job_research = await update_job_research(
        research_id=research_id,
        update_data=job_research_update,
        user_id=current_user.id,
        session=session,
    )
    return updated_job_research
