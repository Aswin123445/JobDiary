import os
from sched import scheduler
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.api.v1 import users,email,profile,research,job_research,job_application
from starlette.middleware.sessions import SessionMiddleware 
from app.core.config import config as settings
from app.utils.email_sent import start_scheduler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    print("Scheduler started")
    
    yield  # FastAPI runs the app here
    
    # Shutdown
app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

app.include_router(users.router,prefix='/v1')
app.include_router(email.router,prefix='/v1')
app.include_router(profile.router,prefix='/v1')
app.include_router(research.router,prefix='/v1')
app.include_router(job_research.router, prefix='/v1')
app.include_router(job_application.router, prefix='/v1')


