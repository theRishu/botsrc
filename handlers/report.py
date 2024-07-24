from aiogram.filters import Command
from aiogram import F, types , Router , Bot
from database import user as db
from constant import m_is_banned , m_is_not_registered ,m_ends_chat
from aiogram.utils.markdown import hbold
from constant import stop_searching
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


report_router = Router()

@report_router.message(Command("report"))
async def handle_report_command(message: types.Message, bot: Bot) -> None:
    try:
        # Fetch user details from the database
        user = await db.select_user(message.from_user.id)
        
        # Ensure the command is a reply to a message
        reported_message = message.reply_to_message
        if not reported_message:
            await message.answer("You need to reply to a partner's message.")
            return

        # Calculate the time difference between the current message and the reported message
        time_diff = message.date - reported_message.date

        # Determine the time threshold based on the user's premium status
        if user.premium  == True:
            time_threshold = 60  # 60 seconds for premium users
        else:
            time_threshold = 30  # 30 seconds for non-premium users

        # Check if the time difference meets the threshold
        if time_diff.total_seconds() > time_threshold:
            await message.answer(f"The message you reported is too old. It must be reported within {time_threshold} seconds.")
            return

        # Check if the user is currently awaiting a match
        if user.request:
            await message.answer(
                "You are waiting for your previous partner to match with you again. "
                "If you want to match with a new partner, you can press /stop and find a new one.",
                reply_markup=stop_searching()
            )
            return

        # Check if the user is currently in a chat
        if user.partner_id:
            # Forward the reported message to the admin
            await bot.copy_message(chat_id=1291389760,from_chat_id=message.from_user.id,message_id=reported_message.message_id)
            await message.answer("This message was Reported",reply_to_message_id=reported_message.message_id)
        else:
            await message.answer("You are not in a chat.")

    except Exception as e:
        await message.answer(f"An error occurred. Please forward this to the admin: {str(e)}")

