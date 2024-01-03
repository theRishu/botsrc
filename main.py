import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import routers_list
from database.setup import initialize_database

async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(*routers_list)
    await initialize_database(reset_db=False)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
