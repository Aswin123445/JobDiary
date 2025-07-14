from pydantic import BaseModel

class EmailVerification(BaseModel):
    username: str
    email: str
    is_email_verified: bool
    
class EmailVerificationResponse(BaseModel):
    user:EmailVerification
    message:str