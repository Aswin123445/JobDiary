
from fastapi import HTTPException, status,BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate, UserLogin
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
    existing_user = await get_user_by_email(user.username, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
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