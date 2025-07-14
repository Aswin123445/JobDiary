from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.schemas.email_schema import EmailVerificationResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.emailservice import verify_email_and_set_verified
router = APIRouter()

@router.get("/verify-email",response_model=EmailVerificationResponse,status_code=status.HTTP_200_OK)
async def create_email_verification_endpoint(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    return await verify_email_and_set_verified(token, db)