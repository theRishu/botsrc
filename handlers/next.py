from aiogram.filters import Command
from aiogram import F, types , Router , Bot
from database import user as db
from constant import m_is_banned , m_is_not_registered ,m_ends_chat
from aiogram.utils.markdown import hbold

from handlers.setting import BUTTON_BACK, BUTTON_UFEMALE, BUTTON_UMALE, BUTTON_UUNKNOWN

from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)



next_router = Router()

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



@next_router.message(Command("next"))
@next_router.message(Command("chat"))
async def command_start_handler(message: types.Message, bot: Bot) -> None:
    try:
        user = await db.select_user(message.from_user.id)
        if not user:
            if await db.is_user_banned(message.from_user.id):
                await message.answer(m_is_banned)
            else:
                await message.answer(m_is_not_registered)
            return

        if user.partner_id:
            await db.delete_match(user.user_id, user.partner_id)
            try:
                await bot.send_message(user.user_id,hbold(m_ends_chat))
            except Exception as e:
                print(str(e))
            try:
                await bot.send_message(user.partner_id,hbold(m_ends_chat))
            except Exception as e:
                print(str(e))
           

        if await db.in_search(message.from_user.id):
            await message.reply("You are already searching for a user.")
        else:
            if user.chat_count % 10 == 9:
                await message.answer("Please follow the /rules, and don't forget to join @Botsphere.")
            await db.enlist_user(message.from_user.id)
            match = await db.get_match(user.user_id, user.gender, user.pgender, user.previous_id)
            if match:
                await db.delist_user(message.from_user.id)
                await db.delist_user(match)
                await db.create_match(user_id=message.from_user.id, partner_id=match)
                try:
                    await bot.send_message(message.from_user.id, "Partner Found!", reply_markup=types.ReplyKeyboardRemove())
                except Exception:
                    pass
                try:
                    await bot.send_message(match, "Partner Found!", reply_markup=types.ReplyKeyboardRemove())
                except Exception:
                    pass
            else:
                await message.answer("Waiting for someone....")

    except Exception as e:
        await message.answer(f"Some error occured forward to admin. {str(e)}")
