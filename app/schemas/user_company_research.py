from typing import Optional, List
from pydantic import BaseModel


class UserCompanyResearchBase(BaseModel):
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


class UserCompanyResearchCreate(UserCompanyResearchBase):
    pass  # all fields required for creation come here


class UserCompanyResearchRead(UserCompanyResearchBase):
    id: int

    class Config:
        orm_mode = True  # Important for SQLModel/ORM compatibility
