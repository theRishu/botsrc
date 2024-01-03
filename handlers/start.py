import datetime
from typing import Optional
from aiogram import Router , types , Bot
from aiogram.filters import CommandStart , CommandObject
from constant import start_buttons
from database import user as db

start_router = Router()



from config import BOT_NAME


NEWCHAT= "✅ Start newchat 💬"

welcome_message = f"""
Welcome to {BOT_NAME} 🚀🌟!

With this bot you can chat with anonymously and the people you chat with have no way to understand who you really are!

Read  the /rules before getting started.

To learn more about us press /help.

Managed by: <a href="https://t.me/BotSphere">BotSphere</a>

To start new chat press /chat or press  {NEWCHAT} button.
"""


start_text= """
With this bot you can chat with anonymously and the people you chat with have no way to understand who you really are!

Choose you preferences with /settings
Report users with  /report
For help press /help.

Also support us by donating some amount to know more how can you donate me press /donate

Spam and illegal stuff are forbidden and punished wiht ban. Read more pressing /rules

Official channel: @BotSphere
"""


@start_router.message(CommandStart())
async def command_start_handler(message:types.Message, command:CommandObject, bot:Bot) -> None:
    ref: Optional[str] = command.args
    try:    
        user = await db.select_user(message.from_user.id)
        if not user:
            if  await db.is_user_banned(message.from_user.id):
                from constant import buy_unban
                x= await  db.check(message.from_user.id)

                if x.ban_expiry > datetime.datetime.now():
                    formatted_expiry = x.ban_expiry.strftime("%d %B %Y at %I:%M %p")
                    await message.answer(f"Sorry, you're banned until {formatted_expiry}.\nTo lift it now, pay @BotSphereSupport.",reply_markup=buy_unban())
                    return
                else:
                    await db.unban_user(message.from_user.id)
                    await message.answer("Good news! Your ban has been lifted.")
            else:
                if ref:
                    if ref.isdigit()==True:
                        await db.update_bonus_count(int(ref))
                       
                await db.add_user(message.from_user.id)
                await message.reply(welcome_message, disable_web_page_preview=True ,
                                     reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="✅ New Chat 💬 ")]], resize_keyboard=True),

                    )
                                
            return
        
        await message.answer(start_text, reply_markup=start_buttons())
        
        
    except Exception as e:
        raise e
