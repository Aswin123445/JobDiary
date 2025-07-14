from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str  
    
class UserRead(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    is_email_verified: bool
class RegisterResponse(BaseModel):
    user: UserRead
    message: str
    
class UserLogin(BaseModel):
    username: str
    password: str

