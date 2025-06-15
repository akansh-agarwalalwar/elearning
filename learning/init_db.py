import asyncio
from database.db import init_db, close_db

async def setup_db():
    await init_db()
    await close_db()

if __name__ == "__main__":
    asyncio.run(setup_db())
    print("Database schema created successfully!") 