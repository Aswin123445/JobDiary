import datetime
from typing import List, Optional
from pydantic import Field
from sqlmodel import Relationship, SQLModel

from app.models.user import User


class UserCompanyResearch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    company_name: str
    mission: Optional[str] = None
    vision: Optional[str] = None
    values: Optional[str] = None
    culture: Optional[str] = None
    recent_news: Optional[str] = None
    competitors: Optional[str] = None
    ceo_name: Optional[str] = None
    location: Optional[str] = None
    services: Optional[str] = None
    total_members: Optional[int] = None
    expected_salary_range: Optional[str] = None
    hr_contact_names: Optional[str] = None

    user: Optional[User] = Relationship(back_populates="company_researches")
    jobs_research: List["UserJobResearch"] = Relationship(back_populates="company_research")


class UserJobResearch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_research_id: int = Field(foreign_key="usercompanyresearch.id")
    job_title: str
    detailed_description: Optional[str] = None
    required_skills: Optional[str] = None
    tech_stack: Optional[str] = None
    team_structure: Optional[str] = None
    challenges: Optional[str] = None

    company_research: Optional[UserCompanyResearch] = Relationship(back_populates="jobs_research")
    applications: List["JobApplication"] = Relationship(back_populates="job_research")


class JobApplication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    job_research_id: int = Field(foreign_key="userjobresearch.id")
    application_date: datetime = Field(default_factory=datetime.utcnow)
    resume_url: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

    user: Optional[User] = Relationship(back_populates="applications")
    job_research: Optional[UserJobResearch] = Relationship(back_populates="applications")