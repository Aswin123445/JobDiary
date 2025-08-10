from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class JobApplicationCreate(BaseModel):
    job_research_id: int
    application_date: Optional[datetime] = None
    resume_url: Optional[HttpUrl] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class JobApplicationRead(JobApplicationCreate):
    id: int
    user_id: int
