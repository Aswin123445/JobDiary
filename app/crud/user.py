from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password,verify_password

# Create a bcrypt hasher

async def create_user(user_data: UserCreate, db: AsyncSession) -> User:
    """Create and save a new user to the database."""
    user_dict = user_data.model_dump(exclude_unset=True)
    # Hash the plain password
    if user_dict['password']:
        hashed_pw = hash_password(user_dict['password'])
        user_dict['hashed_password'] = hashed_pw
    else :
        user_dict['is_email_verified'] = True  #

    # Create a new User object (DB model)
    user_dict.pop('password', None)  # Remove plain password
    user = User(**user_dict)

    # Add the user to the DB session
    db.add(user)
    # Commit the transaction
    await db.commit()
    # Refresh to get generated fields like id, created_at
    await db.refresh(user)

    return user

async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    """Fetch a user from the DB by username."""
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()

def check_password(user: User, password: str) -> bool:
    """Check if the provided password matches the user's hashed password."""
    return verify_password(password, user.hashed_password)
