
from fastapi import HTTPException, status,BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate
from app.crud.user import create_user,get_user_by_username
from app.services.emailservice import send_verification_email
from app.utility.create_email_verification_token import create_email_verification_token
async def register_user(
    user: UserCreate,
    db: AsyncSession,
    background_tasks: BackgroundTasks
):
    existing_user = await get_user_by_username(user.username, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    new_user = await create_user(user, db)
    token = create_email_verification_token(new_user.email)
    background_tasks.add_task(send_verification_email, new_user.email, token)
    return {"user": new_user, "message": "User created successfully. Please check your email to verify your account."}