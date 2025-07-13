# app/routes/user_routes.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate,UserRead
from app.services.user_services import register_user
from app.db.session import get_db  

router = APIRouter()

@router.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def  create_user_endpoint(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await register_user(user, db)