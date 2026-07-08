import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.models import Base
from app.db.session import engine

async def init_db():
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
