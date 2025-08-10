from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.job_application import JobApplicationCreate, JobApplicationRead
from app.services.job_application import create_job_application, delete_job_application
from app.utils.get_current_user import get_current_user

router = APIRouter(prefix="/job-appliation", tags=["job_application"])

@router.post("/", response_model=JobApplicationRead, status_code=status.HTTP_201_CREATED)
async def create_job_application_endpoint(
    job_application_in: JobApplicationCreate,
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    job_application = await create_job_application(
        data=job_application_in,
        user_id=current_user.id,
        session=session,
    )
    return job_application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_application_endpoint(
    application_id: int ,
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    await delete_job_application(
        application_id=application_id,
        user_id=current_user.id,
        session=session,
    )
    return None
