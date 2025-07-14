from datetime import timedelta
from app.utility.jwt import create_access_token
def create_email_verification_token(email: str) -> str:
    return create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=5)  
    )
    