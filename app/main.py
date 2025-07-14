from fastapi import FastAPI
from app.api.v1 import users
from app.api.v1 import email

app = FastAPI()

app.include_router(users.router,prefix='/users')
app.include_router(email.router,prefix='/email')
