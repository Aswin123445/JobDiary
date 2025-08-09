from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password,verify_password
from app.models.profile import Profile

# Create a bcrypt hasher

async def create_user(user_data: UserCreate, db: AsyncSession) -> User:
    """Create and save a new user to the database, along with a profile."""
    user_dict = user_data.model_dump(exclude_unset=True)

    # Hash the plain password if provided
    if user_dict.get('password'):
        hashed_pw = hash_password(user_dict['password'])
        user_dict['hashed_password'] = hashed_pw
    else:
        user_dict['is_email_verified'] = True  

    # Remove plain password before saving
    user_dict.pop('password', None)

    # Create and persist user
    user = User(**user_dict)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Create a profile linked to this user
    profile = Profile(
        user_id=user.id,
        name=user.username,  # or another default
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)

    return user


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    """Fetch a user from the DB by username."""
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()

def check_password(user: User, password: str) -> bool:
    """Check if the provided password matches the user's hashed password."""
    return verify_password(password, user.hashed_password)

from sqlmodel import select

async def get_profile_by_user_id(user_id: int, db: AsyncSession):
    statement = select(Profile).where(Profile.user_id == user_id)
    result = await db.execute(statement)
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


