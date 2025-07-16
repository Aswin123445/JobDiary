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
class RegisterResponse(BaseModel):
    user: UserRead
    message: str
    
class UserLogin(BaseModel):
    email: str
    password: str
    
class UserSignInResponse(BaseModel):
    user: UserRead
    access_token: str
    token_type: str = "bearer"

