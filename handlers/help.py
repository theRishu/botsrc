from aiogram.filters import Command
from aiogram import types, Router
from database import user as db
from constant import buy_vip, help_text ,rules_text ,channel_button,commands_message , donate_message , contact_admin

help_router = Router()




@help_router.message(Command("help"))
async def help_handler(message: types.Message ) -> None:
    try:
        await message.reply(help_text)
    except Exception as e:
        await message.answer(str(e))
    


@help_router.message(Command(commands=["rules", "rules"]))
async def rules_router(message: types.Message ) -> None:
    await message.reply(rules_text ,reply_markup=channel_button())
    
    



@help_router.message(Command(commands=["buy_vip", "vip"]))
async def rules_router(message: types.Message ) -> None:
    await message.reply("For purchasing vip contact @BotsphereSupport" , reply_markup=buy_vip())
    


@help_router.message(Command(commands=["commands", "commands"]))
async def rules_router(message: types.Message ) -> None:
    await message.reply(commands_message)
    
   

@help_router.message(Command("donate"))
async def rules_router(message: types.Message ) -> None:
    await message.answer(donate_message,disable_web_page_preview=True ,reply_markup=contact_admin())
    
    
   
   