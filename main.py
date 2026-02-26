import asyncio
from aiogram import Bot, Dispatcher , types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import routers_list
from database.setup import initialize_database
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from middlewares.url import URLMiddleware

from sqlalchemy import text
from database.setup import engine


async def setcommands(bot):
    commands = [
        types.BotCommand(command="/start", description="To start new chat."),
        types.BotCommand(command="/end", description="To end this chat."),
        types.BotCommand(command="/next", description="End current chat and start new chat."),
        types.BotCommand(command="/help", description="for help."),
        types.BotCommand(command="/settings", description="user settings."),
        types.BotCommand(command="/reopen", description="reopen previous chat"),
        types.BotCommand(command="/report", description="to report this content."),
        types.BotCommand(command="/issue", description="write to developer")
        ]
    await bot.send_message(1291389760 ,"Bot Started.")
    await bot.delete_my_commands()
    await bot.set_my_commands(commands)


def register_global_middlewares(dp: Dispatcher , bot:Bot):
    middleware_types = [URLMiddleware(bot)]
    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        


async def x(engine):
    async with engine.begin() as conn:
        # Step 1: Add the Column with a Default Value of None
        await conn.run_sync(lambda conn: conn.execute(text('ALTER TABLE users ADD COLUMN reopen BOOLEAN DEFAULT TRUE')))
        await conn.run_sync(lambda conn: conn.execute(text('ALTER TABLE users ADD COLUMN request BOOLEAN DEFAULT FALSE')))

        # Step 2: Update Existing Rows
        await conn.run_sync(lambda conn: conn.execute(text("UPDATE users SET reopen = TRUE, request = FALSE")))


from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8084)
    await site.start()
    print("Web server started on port 8081")

async def main():
    try:
        await x(engine)
    except Exception:
        pass
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    storage = MemoryStorage()
    await setcommands(bot)
    dp = Dispatcher(storage=storage)
    dp.include_routers(*routers_list)
    register_global_middlewares(dp , bot)
    await initialize_database(reset_db=False)
    
    # Start web server in the background
    await start_web_server()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
