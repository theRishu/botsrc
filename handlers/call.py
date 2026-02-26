from aiogram.filters import Command
from aiogram import types, Router, Bot
from aiogram.types import (
    Message,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

import aiohttp
from database import user as db
from constant import (
    m_is_banned,
    m_is_not_registered,
)

# ================= CONFIG =================

from config import WEB_URL
call_router = Router()

# =========================================


@call_router.message(Command("call"))
async def command_call_handler(message: Message, bot: Bot):
    try:
        # 1. Fetch user from DB
        user = await db.select_user(message.from_user.id)

        # 2. Registration / ban checks
        if not user:
            if await db.is_user_banned(message.from_user.id):
                await message.answer(m_is_banned)
            else:
                await message.answer(m_is_not_registered)
            return

        # 3. Partner (chat) state enforcement
        if not user.partner_id:
            await message.answer("❌ You are not currently in an active chat.")
            return

        # Request new call session from the FastApi Server
        api_url = f"{WEB_URL}/api/create_call"
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url) as resp:
                data = await resp.json()
        
        caller_token = data.get("caller_token")
        callee_token = data.get("callee_token")
        
        # Build links
        link1 = f"{WEB_URL}/join/{caller_token}"
        link2 = f"{WEB_URL}/join/{callee_token}"

        # 1. Send Caller Link to the user who typed /call
        caller_kb = InlineKeyboardBuilder()
        caller_kb.row(InlineKeyboardButton(text="📞 START CALL", url=link1))
        
        await message.answer(
            "✅ *Call session initialized*\n\nOpen the link below in your browser to start the call.",
            reply_markup=caller_kb.as_markup(),
            parse_mode="Markdown"
        )

        # 2. Send Callee Link to the partner
        callee_kb = InlineKeyboardBuilder()
        callee_kb.row(InlineKeyboardButton(text="📲 JOIN AS PARTNER", url=link2))
        
        await bot.send_message(
            chat_id=user.partner_id,
            text=f"📞 *Incoming Call*\n\nYour partner has started a video call. Join using the button below:",
            reply_markup=callee_kb.as_markup(),
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.answer(f"⚠️ Internal error: {e}")


