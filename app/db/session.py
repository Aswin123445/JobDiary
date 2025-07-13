from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import config

#for sync version for alembic migrations 
from sqlalchemy import create_engine
sync_url = config.database_url.replace('postgresql+asyncpg','postgresql')
syncengine = create_engine(sync_url)

#for fastapi async version 
engine = create_async_engine(config.database_url, echo=True)
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession: # type: ignore
    async with async_session() as session:
        yield session