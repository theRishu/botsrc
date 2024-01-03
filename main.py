import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import routers_list
from database.base import Base

from config import BOT_NAME
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
DB_URI  = f"postgresql+asyncpg://postgres:1234@localhost:5432/{BOT_NAME}"

engine = create_async_engine(DB_URI,
    query_cache_size=1200,
    pool_size=20,
    max_overflow=200,
    future=True,
    echo=False
    )
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def initialize_database(reset_db=False):
    if reset_db:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            print("DB Dropped..")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(*routers_list)
    await initialize_database(reset_db=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
