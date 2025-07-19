from pydantic import Field,EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict 

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    database_url: str = Field(default="postgresql:///./test.db")
    JWT_SECRET_KEY: str
    SESSION_SECRET_KEY:str
    JWT_ALGORITHM: str 
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int 

    MAIL_USERNAME: EmailStr
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_FROM_NAME: str = "Job Diary"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    GOOGLE_CLIENT_ID:str 
    GOOGLE_CLIENT_SECRET:str
    GOOGLE_REDIRECT_URL:str
config = Settings()
print(config.GOOGLE_CLIENT_ID)