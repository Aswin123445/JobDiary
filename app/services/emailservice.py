from fastapi import HTTPException,status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import config as settings
from fastapi_mail.email_utils import DefaultChecker
from jinja2 import Template
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt,JWTError
from sqlmodel import select
from app.models.user import User

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
)

async def send_verification_email(to_email: str, token: str):
    verify_link = f"http://localhost:8000/email/verify-email?token={token}"
    template_path = Path(__file__).parent / "templates" / "verify_email.html"

    html = Template(template_path.read_text()).render(link=verify_link)

    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[to_email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    
async def verify_email_and_set_verified(token: str,db: AsyncSession):
    try :
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email = payload.get("sub")
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email not found"
            )
        #find user by email
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_email_verified = True 
        await db.commit()
        return {'user':user,'message':'email hasbeen successfully verified'}
    except JWTError:
        raise HTTPException(status_code=400, detail="❌ Invalid or expired token")
