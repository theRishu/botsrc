import datetime
from typing import Optional
from aiogram import Router , types , Bot
from aiogram.filters import CommandStart , CommandObject
from constant import start_buttons
from database import user as db
from aiogram.utils.markdown import hbold



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

BUTTON_UFEMALE = types.InlineKeyboardButton(text="Female 👩", callback_data="FFF"),
BUTTON_UMALE = types.InlineKeyboardButton(text="Male 👦", callback_data="MMM"),




@start_router.message(CommandStart())
async def command_start_handler(message: types.Message, bot: Bot) -> None:
    user = await db.select_user(message.from_user.id)
    if user:
        if user.partner_id:
            await message.answer("You are already in a chat.", reply_markup=types.ReplyKeyboardRemove())
            return

        if await db.in_search(message.from_user.id):
            await message.reply("You are already searching for a user. Please wait.")
            return


        if user.chat_count % 10 == 9:
            await message.answer("Please follow the /rules, and don't forget to join @Botsphere.")
        else:
            pass


        await db.enlist_user(message.from_user.id)

        match = await db.get_match(user.user_id, user.gender, user.pgender, user.previous_id)
        if match:
            await db.delist_user(message.from_user.id)
            await db.delist_user(match)
            await db.create_match(user_id=message.from_user.id, partner_id=match)
            try:
                await bot.send_message(message.from_user.id, hbold("Partner Found!"), reply_markup=types.ReplyKeyboardRemove())
            except Exception as e:
                print(str(e))

            try:
                await bot.send_message(match, hbold("Partner Found!"), reply_markup=types.ReplyKeyboardRemove())
            except Exception as e:
                print(str(e))
        else:
            await message.answer("🚀 Start looking for a partner for you...")

    else:
        if await db.is_user_banned(message.from_user.id):
            x = await db.check(message.from_user.id)
            if x.ban_expiry > datetime.now():
                formatted_expiry = x.ban_expiry.strftime("%d %B %Y at %I:%M %p")
                await message.answer(f"Sorry, you're banned until {formatted_expiry}.\nTo lift it now, pay @BotSphereSupport.", reply_markup=buy_unban())
                return
            else:
                await db.unban_user(message.from_user.id)
                await message.answer("Good news! Your ban has been lifted.")
        else:
            await message.answer("To use this bot, you need to set up your gender. Please Select your gender.",
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[BUTTON_UMALE, BUTTON_UFEMALE],resize_keyboard=True))




from aiogram import F
from aiogram import types


@start_router.callback_query(F.data.in_(["MMM", "FFF"]))
async def show_gender(call: types.CallbackQuery):
    try:
        gender = "M" if call.data == "MMM" else "F" if call.data == "FFF" else None
        user_id = call.from_user.id
        await db.add_user(user_id ,gender)
        await call.message.edit_text("Everything is set. Now press /start to search user.")

    except Exception as e:
        await call.message.edit_text(str(e) ,parse_mode=None)
