
from fastapi import HTTPException, status,BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import OAuthUserCreate, UserCreate, UserLogin
from app.crud.user import check_password, create_user,get_user_by_email
from app.services.emailservice import send_verification_email
from app.utils.create_email_verification_token import create_email_verification_token
from app.utils.jwt import create_access_token
from datetime import timedelta
async def register_user(
    user: UserCreate,
    db: AsyncSession,
    background_tasks: BackgroundTasks
):
    existing_user = await get_user_by_email(user.email, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already taken"
        )

    new_user = await create_user(user, db)
    token = create_email_verification_token(new_user.email)
    background_tasks.add_task(send_verification_email, new_user.email, token)
    return {"user": new_user, "message": "User created successfully. Please check your email to verify your account."}

async def login_user(
    user: UserLogin,
    db: AsyncSession
):
    existing_user = await get_user_by_email(user.email, db)
    print(existing_user)
    if not existing_user or not check_password(existing_user,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if existing_user.is_active is False or existing_user.is_email_verified is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive. Please verify your email."
        )
    token_data = existing_user.email
    token = create_access_token(data={"sub":token_data}, expires_delta = timedelta(minutes=30))
    return {
        "user": existing_user,
        "access_token": token,
        "token_type": "bearer"
    }
    
async def handle_google_auth(user:dict, db: AsyncSession):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    
    user_info = user.get('userinfo')
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User info not found"
        )
    
    email = user_info.get('email')
    name = user_info.get('name')
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not found in user info"
        )

    existing_user = await get_user_by_email(email, db)
    if not existing_user:
        # Create a new user if they don't exist
        new_user = OAuthUserCreate(username=name, email=email, password=None)  # Password is None for OAuth users
        existing_user = await create_user(new_user, db)

    token_data = existing_user.email
    token = create_access_token(data={"sub": token_data}, expires_delta=timedelta(minutes=30))
    
    return {
        "user": existing_user,
        "access_token": token,
        "token_type": "bearer"
    }