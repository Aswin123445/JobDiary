# app/routes/user_routes.py
from fastapi import APIRouter, Depends, status,BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import RegisterResponse, UserCreate,UserRead
from app.services.user_services import register_user
from app.db.session import get_db  

router = APIRouter()

@router.post("/users/", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def  create_user_endpoint(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    return await register_user(user, db,background_tasks)

