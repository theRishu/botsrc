from aiogram.filters import Command
from aiogram import F, types , Router , Bot
from database import user as db
from constant import m_is_banned , m_is_not_registered ,m_ends_chat
from aiogram.utils.markdown import hbold
from constant import stop_searching
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
report_router = Router()


@report_router.message(Command("report"))
async def command_start_handler(message: types.Message, bot: Bot) -> None:
    try:
        user = await db.select_user(message.from_user.id)
        if not user:
            if await db.is_user_banned(message.from_user.id):
                await message.answer(m_is_banned)
            else:
                await message.answer(m_is_not_registered)
            return
        
        reported_message = message.reply_to_message
        if reported_message is None:
           await message.answer("Reported")
           return

        
        if user.request == True:
            await message.answer("You are waiting so your previous partner can match with you again. If You want to match  new partner You can press /stop and find new one." , reply_markup=stop_searching())
            return

       
        if user.partner_id:
            await bot.copy_message(1291389760, from_chat_id= message.from_user.id, message_id=message.reply_to_message.message_id)
            await message.answer("Reported")

        else:
            await message.answer("You are not in chat.")

    except Exception as e:
        await message.answer(f"Some error occured forward to admin. {str(e)}")
