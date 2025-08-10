import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
from app.core.config import config as settings

async def send_email(to: str, subject: str, body: str):
    # Prepare the email
    msg = MIMEMultipart()
    msg["From"] = settings.MAIL_USERNAME
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Send email in a separate thread so it doesn't block
    def _send():
        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
            server.starttls()
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.sendmail(settings.MAIL_USERNAME, to, msg.as_string())

    await asyncio.to_thread(_send)
