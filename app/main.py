from fastapi import FastAPI
from app.api.v1 import users,email
from starlette.middleware.sessions import SessionMiddleware 
from app.core.config import config as settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

app.include_router(users.router,prefix='/v1')
app.include_router(email.router,prefix='/v1')
