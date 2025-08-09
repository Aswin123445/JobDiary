# app/models/profile.py
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import DateTime

class Profile(SQLModel, table=True):
    __tablename__ = "profiles"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)

    name: str
    bio: Optional[str] = None
    profile_url: Optional[str] = None
    current_job: Optional[str] = None
    company: Optional[str] = None
    skills: Optional[str] = None  # Could be JSON in the future

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True))
    )

    # Relationship to User
    user: Optional["User"] = Relationship(back_populates="profile") # type: ignore

# And in your User model, add:
# profile: Optional["Profile"] = Relationship(back_populates="user")
