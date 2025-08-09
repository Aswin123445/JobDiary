from sqlmodel import SQLModel, Field , Column
from typing import Literal, Optional
from datetime import datetime, timezone
from sqlalchemy import DateTime
from app.models.enam import AuthProvider

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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),sa_column=Column(DateTime(timezone=True)))
