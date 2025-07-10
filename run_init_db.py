# run_init_db.py
import asyncio
from app.db.init_db import init_db

asyncio.run(init_db())
