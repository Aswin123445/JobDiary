from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import config
from sqlalchemy.orm import declarative_base

engine = create_async_engine(config.database_url, echo=True)
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base() 

async def get_db() -> AsyncSession: # type: ignore
    async with async_session() as session:
        yield session