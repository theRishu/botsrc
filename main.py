import asyncio
from aiogram import Bot, Dispatcher , types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import routers_list
from database.setup import initialize_database

from sqlalchemy import text
from database.setup import engine


async def setcommands(bot):
    commands = [
        types.BotCommand(command="/start", description="To start new chat."),
        types.BotCommand(command="/end", description="To end this chat."),
        types.BotCommand(command="/next", description="End current chat and start new chat."),
        types.BotCommand(command="/help", description="for help."),
        types.BotCommand(command="/settings", description="user settings."),
        types.BotCommand(command="/reopen", description="reopen previous chat")
        ]
    await bot.delete_my_commands()
    await bot.set_my_commands(commands)


async def x(engine):
    async with engine.begin() as conn:
        # Step 1: Add the Column with a Default Value of None
        await conn.run_sync(lambda conn: conn.execute(text('ALTER TABLE users ADD COLUMN reopen BOOLEAN DEFAULT TRUE')))
        await conn.run_sync(lambda conn: conn.execute(text('ALTER TABLE users ADD COLUMN request BOOLEAN DEFAULT FALSE')))

        # Step 2: Update Existing Rows
        await conn.run_sync(lambda conn: conn.execute(text("UPDATE users SET reopen = TRUE, request = FALSE")))



async def main():
    try:
        await x(engine)
    except Exception as e:
        print(str(e))
   
    

    
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    await setcommands(bot)

    
    dp = Dispatcher(storage=storage)
    dp.include_routers(*routers_list)
    await initialize_database(reset_db=False)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
