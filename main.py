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
        types.BotCommand(command="/help", description="for help.")
        ]
    await bot.delete_my_commands()
    await bot.set_my_commands(commands)


async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML, protect_content=False)
    storage = MemoryStorage()
    await setcommands(bot)
    dp = Dispatcher(storage=storage)
    dp.include_routers(*routers_list)
    await initialize_database(reset_db=False)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
