from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))