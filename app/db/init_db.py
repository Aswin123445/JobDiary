from sqlmodel import SQLModel
from app.db.session import engine  # keep your engine from create_async_engine
from app.models import user, research ,profile # important: import models before running

async def init_db():
    print("🔧 Creating tables...")
    print("🔎 Tables found:", SQLModel.metadata.tables.keys())

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    print("✅ Tables created.")
