# app/schemas/profile.py
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


# Shared properties (common fields)
class ProfileBase(BaseModel):
    name: str
    bio: Optional[str] = None
    profile_url: Optional[HttpUrl] = None  # Validated as URL
    current_job: Optional[str] = None
    company: Optional[str] = None
    skills: Optional[str] = None


# Schema for updating a profile
class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    profile_url: Optional[HttpUrl] = None
    current_job: Optional[str] = None
    company: Optional[str] = None
    skills: Optional[str] = None


# Schema for reading a profile (includes DB-only fields)
class ProfileRead(ProfileBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # needed when returning ORM/SQLModel objects
