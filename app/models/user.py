from sqlmodel import Relationship, SQLModel, Field , Column
from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy import DateTime
from app.models.enam import AuthProvider
from app.models.profile import Profile
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    hashed_password:Optional[str] = None # This field is optional for OAuth users
    is_active: bool = True
    is_superuser: bool = False
    auth_provider: AuthProvider = Field(default=AuthProvider.email, nullable=True)
    is_email_verified: bool = Field(default=False)
    company_researches: List["UserCompanyResearch"] = Relationship(back_populates="user") # type: ignore
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),sa_column=Column(DateTime(timezone=True)))
    profile: Optional[Profile] = Relationship(back_populates="user")
    applications: List["JobApplication"] = Relationship(back_populates="user") # type: ignore


