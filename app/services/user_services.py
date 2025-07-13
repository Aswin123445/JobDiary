
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate
from app.crud.user import create_user,get_user_by_username
async def register_user(
    user: UserCreate,
    db: AsyncSession
):
    existing_user = await get_user_by_username(user.username, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    new_user = await create_user(user, db)
    return new_user