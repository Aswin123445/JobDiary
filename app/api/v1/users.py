# app/routes/user_routes.py
from fastapi import APIRouter, Depends, status,BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import RegisterResponse, UserCreate, UserLogin, UserSignInResponse
from app.services.user_services import handle_google_auth, login_user, register_user
from app.db.session import get_db  
from fastapi import Request
from app.core.google_oauth import oauth

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

@router.get("/google/login")
async def google_login_endpoint(request: Request):
    redirect_uri = request.url_for('google_auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback", name="google_auth_callback" ,response_model=UserSignInResponse, status_code=status.HTTP_200_OK)
async def google_callback_endpoint(request: Request, db: AsyncSession = Depends(get_db)):   
    user = await oauth.google.authorize_access_token(request)
    return await handle_google_auth(user, db)



