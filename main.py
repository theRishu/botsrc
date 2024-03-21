import asyncio
from aiogram import Bot, Dispatcher , types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import routers_list
from database.setup import initialize_database


async def setcommands(bot):
    commands = [
        types.BotCommand(command="/start", description="To start new chat."),
        types.BotCommand(command="/end", description="To end this chat."),
        types.BotCommand(command="/next", description="End current chat and start new chat."),
        types.BotCommand(command="/help", description="for help."),
        types.BotCommand(command="/settings", description="user settings.")
        ]
    await bot.delete_my_commands()
    await bot.set_my_commands(commands)



import asyncio
from sqlalchemy import text
from database.setup import engine

import sqlalchemy
from sqlalchemy import text

async def add_reopen(engine):
    async with engine.begin() as conn:
        try:
            # Step 1: Add the Columns with Default Values if they don't exist
            await conn.run_sync(lambda conn: conn.execute(text('ALTER TABLE IF NOT EXISTS users ADD COLUMN reopen BOOLEAN DEFAULT TRUE')))

            # Step 2: Update Existing Rows
            await conn.run_sync(lambda conn: conn.execute(text('UPDATE users SET reopen = True WHERE reopen IS NULL')))

        except Exception as e:
          
            print(f"An error occurred: {e}")

async def add_request(engine):
    async with engine.begin() as conn:
        try:
            # Step 1: Add the Column with a Default Value of False if it doesn't exist
            await conn.run_sync(lambda conn: conn.execute(text('ALTER TABLE IF NOT EXISTS users ADD COLUMN request BOOLEAN DEFAULT FALSE')))

            # Step 2: Update Existing Rows
            await conn.run_sync(lambda conn: conn.execute(text('UPDATE users SET request = FALSE WHERE can_use IS NULL')))
        except Exception as e:
            print(f"An error occurred: {e}")









async def main():
    await add_reopen(engine)
    await add_request(engine)
    

    
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML, protect_content=True)
    storage = MemoryStorage()
    await setcommands(bot)

    
    dp = Dispatcher(storage=storage)
    dp.include_routers(*routers_list)
    await initialize_database(reset_db=False)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
