from typing import Optional
from pydantic import BaseModel, EmailStr ,field_validator, Field
from typing import Annotated
from app.utils.validators.user_validators import validate_password_helper, validate_username_helper
class UserBase(BaseModel):
    username: Annotated[
        str, 
        Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9][A-Za-z0-9 .'\-]{1,48}[A-Za-z0-9]$")
    ]
    email: EmailStr
    @field_validator('username')
    def validate_username(cls, value:str) -> str:
        if value:
            return validate_username_helper(value)
        raise
class UserCreate(UserBase):
    password: str 
    
    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if value:
           return validate_password_helper(value)
        raise ValueError("Password cannot be empty.")
        
     
class OAuthUserCreate(UserBase): 
    password:Optional[str] = None
    auth_provider: str = "google"  
    
class UserRead(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    
class RegisterResponse(BaseModel):
    user: UserRead
    message: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if value:
            return validate_password_helper(value)
        raise ValueError("Password cannot be empty.")
    
class UserSignInResponse(BaseModel):
    user: UserRead
    access_token: str
    token_type: str = "bearer"

