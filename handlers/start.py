import datetime
from typing import Optional
from aiogram import Router , types , Bot
from aiogram.filters import CommandStart , CommandObject
from constant import start_buttons
from database import user as db
from aiogram.utils.markdown import hbold
from constant import stop_searching , channel_button

start_router = Router()

from config import BOT_NAME



BUTTON_UFEMALE = types.InlineKeyboardButton(text="Female ♀️", callback_data="FFF"),
BUTTON_UMALE = types.InlineKeyboardButton(text="Male ♂️", callback_data="MMM"),


@start_router.message(CommandStart(deep_link=True))
async def handler(message: types.Message, command: CommandObject):
    ref = command.args
    user = await db.select_user(message.from_user.id)
    if not user:
        if ref and ref.isdigit() and await db.is_user_present(int(ref)):
            await db.update_bonus_count(int(ref))
        await message.answer("To use this bot, you need to set up your gender. Please Select your gender.",reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[BUTTON_UMALE, BUTTON_UFEMALE],resize_keyboard=True))
    else:
        await message.answer("Please press /start to chat.")













@start_router.message(CommandStart())
async def command_start_handler(message: types.Message, bot: Bot) -> None:
    user = await db.select_user(message.from_user.id)
    if user:

        if user.request == True:
            await message.answer("You are waiting so your previous partner can match with you again. If You want to match  new partner You can press /stop and find new one." , reply_markup=stop_searching())
            return
        if user.partner_id:
            await message.answer("You are already in a chat.", reply_markup=types.ReplyKeyboardRemove())
            return
        if await db.in_search(message.from_user.id):
            await message.reply("You are already searching for a user. Please wait." ,reply_markup=stop_searching())
            return


        if user.chat_count % 10 == 9:
            await message.answer("Please follow the /rules, and don't forget to join @Botsphere.")

        elif user.chat_count > 50:
            result = await bot.get_chat_member("@Botsphere", user.user_id)
            if result.status not  in ["member", "creator", "administrator"]:
                await message.answer("To use this bot further , You need to join @Botsphere." , reply_markup=channel_button())
                return 
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
            await message.answer("🚀 Start looking for a partner for you..." , reply_markup=stop_searching())

    else:
        if await db.is_user_banned(message.from_user.id):
            x = await db.check(message.from_user.id)
            if x.ban_expiry > datetime.datetime.now():
                formatted_expiry = x.ban_expiry.strftime("%d %B %Y at %I:%M %p")
                await message.answer(f"Sorry, you're banned.")
                return
            else:
                await db.unban_user(message.from_user.id)
                await message.answer("Good news! Your ban has been lifted.")
        else:
            botname = await bot.get_me()
            await message.answer(f"""
            <b> Welcome to @{botname.username}</b>!

To use this bot, you need to set up your gender. Please Select your gender.""",
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[BUTTON_UMALE ,BUTTON_UFEMALE],
                
                resize_keyboard=True))




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
        await db.update_user_pgender(call.from_user.id, data)
