# app/routes/user_routes.py
from fastapi import APIRouter, Depends, status,BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import RegisterResponse, UserCreate, UserLogin,UserRead, UserSignInResponse
from app.services.user_services import login_user, register_user
from app.db.session import get_db  

router = APIRouter(prefix='/auth')

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def  create_user_endpoint(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    return await register_user(user, db,background_tasks)

@router.post("/login/",response_model=UserSignInResponse, status_code=status.HTTP_200_OK)
async def login_user_endpoint(
    user: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    return await login_user(user, db)
