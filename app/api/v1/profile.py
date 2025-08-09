from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.profile import ProfileRead, ProfileUpdate
from app.db.session import get_db
from app.models.user import User
from app.services.user_services import get_user_profile, update_user_profile
from app.utils.get_current_user import get_current_user

router = APIRouter(prefix="/user")

@router.get("/profile", response_model=ProfileRead, status_code=status.HTTP_200_OK)
async def get_profile(
    current_user: User = Depends(get_current_user),  # usually from auth token, or Depends(get_current_user)
    db: AsyncSession = Depends(get_db)
):
    profile = await get_user_profile(user = current_user, db=db)
    # You can add background tasks here if needed
    return profile


@router.put("/profile", response_model=ProfileRead)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    updated_profile = await update_user_profile(db, current_user.id, profile_data)
    return updated_profile
