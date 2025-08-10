from pydantic import BaseModel
from typing import Optional

class UserJobResearchCreate(BaseModel):
    company_research_id: int
    job_title: str
    detailed_description: Optional[str] = None
    required_skills: Optional[str] = None
    tech_stack: Optional[str] = None
    team_structure: Optional[str] = None
    challenges: Optional[str] = None

class UserJobResearchUpdate(BaseModel):
    job_title: Optional[str] = None
    detailed_description: Optional[str] = None
    required_skills: Optional[str] = None
    tech_stack: Optional[str] = None
    team_structure: Optional[str] = None
    challenges: Optional[str] = None

class UserJobResearchRead(UserJobResearchCreate):
    id: int
