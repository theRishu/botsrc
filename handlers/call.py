from aiogram.filters import Command
from aiogram import types, Router, Bot
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    WebAppInfo,
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
    await message.answer(WEB_URL)
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
            await message.answer("❌ *No Active Chat*\n\nYou can only start a call with someone you are currently chatting with.", parse_mode="Markdown")
            return

        # Request new call session from the FastApi Server
        api_url = f"{WEB_URL}/api/create_call"
        payload = {
            "caller_id": str(message.from_user.id),
            "callee_id": str(user.partner_id)
        }
        headers = {"ngrok-skip-browser-warning": "any"}
        
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(api_url, json=payload) as resp:
                if resp.status != 200:
                    await message.answer("⚠️ *Connection Unavailable*\n\nPlease try again in a few moments.", parse_mode="Markdown")
                    return
                data = await resp.json()
        
        caller_token = data.get("caller_token")
        callee_token = data.get("callee_token")
        
        # Build premium links
        recovery_params = f"?caller_id={message.from_user.id}&callee_id={user.partner_id}"
        link1 = f"{WEB_URL}/join/{caller_token}{recovery_params}"
        link2 = f"{WEB_URL}/join/{callee_token}{recovery_params}"

        # 1. Start Button for Caller
        caller_kb = InlineKeyboardBuilder()
        caller_kb.row(InlineKeyboardButton(text="Enter Session", url=link1))
        
        await message.answer(
            "*Video Session*\n\nYour secure connection is established. Select below to enter.",
            reply_markup=caller_kb.as_markup(),
            parse_mode="Markdown"
        )

        # 2. Invitation to Partner
        callee_kb = InlineKeyboardBuilder()
        callee_kb.row(InlineKeyboardButton(text="Join Session", url=link2))
        
        await bot.send_message(
            chat_id=user.partner_id,
            text=f"*Incoming Session Request*\n\nYour partner has initiated a private video session.",
            reply_markup=callee_kb.as_markup(),
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Error in call.py: {e}")
        await message.answer("⚠️ *System Maintenance*\n\nWe're currently performing optimization. Please stay tuned.", parse_mode="Markdown")


