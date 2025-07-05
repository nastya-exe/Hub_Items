from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import Base

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/ip_bot"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
