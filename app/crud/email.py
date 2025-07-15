from app.models.user import User
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
async def get_user_by_email(email:str, db: AsyncSession) -> User | None:
    """Fetch a user from the DB by email."""
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none() 
    if not user: 
        return None
    user.is_email_verified = True
    await db.commit() 
    return user