from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password

# Create a bcrypt hasher


async def create_user(user_data: UserCreate, db: AsyncSession) -> User:
    """Create and save a new user to the database."""
    # Hash the plain password
    hashed_pw = hash_password(user_data.password)

    # Create a new User object (DB model)
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw
    )

    # Add the user to the DB session
    db.add(user)

    # Commit the transaction
    await db.commit()

    # Refresh to get generated fields like id, created_at
    await db.refresh(user)

    return user

async def get_user_by_username(username: str, db: AsyncSession) -> User | None:
    """Fetch a user from the DB by username."""
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()
