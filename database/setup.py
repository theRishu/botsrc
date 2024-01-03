from  .base import Base
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from config import BOT_NAME

DB_URI  = f"postgresql+asyncpg://postgres:1234@localhost:5432/{BOT_NAME}"

engine = create_async_engine(DB_URI,
    query_cache_size=1200,
    pool_size=20,
    max_overflow=200,
    future=True,
    echo=False)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def initialize_database(reset_db=False):
    if reset_db:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            print("DB Dropped..")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
