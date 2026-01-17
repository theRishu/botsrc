from aiogram.filters import Command
from aiogram import types, Router, Bot
from aiogram.types import (
    Message,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

import base64
import hmac
import hashlib
import uuid

from database import user as db
from constant import (
    m_is_banned,
    m_is_not_registered,
)

# ================= CONFIG =================

SECRET_KEY = b"SUPER_SECRET_HMAC_KEY_2026"
WEB_URL = "https://lovetender.in"

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

        # 4. Generate secure call session
        tag = "None"
        meta = f"partner:{user.partner_id}"

        rid = str(uuid.uuid4())[:8]

        raw_payload = f"{message.from_user.id}|{tag}|{meta}"
        payload = (
            base64.urlsafe_b64encode(raw_payload.encode())
            .decode()
            .rstrip("=")
        )

        signature = hmac.new(
            SECRET_KEY,
            payload.encode(),
            hashlib.sha256
        ).hexdigest()[:8]

        base_url = f"{WEB_URL}/go/{rid}?p={payload}&h={signature}"

        # 5. Caller keyboard
        caller_kb = InlineKeyboardBuilder()
        caller_kb.row(
            InlineKeyboardButton(
                text="📞 START CALL",
                url=f"{base_url}&role=caller"
            )
        )

        await message.answer(
            "✅ **Call session initialized**\n\nClick below to start the call.",
            reply_markup=caller_kb.as_markup(),
            parse_mode="Markdown"
        )

        # 6. Callee keyboard (partner)
        callee_kb = InlineKeyboardBuilder()
        callee_kb.row(
            InlineKeyboardButton(
                text="📲 JOIN CALL",
                url=f"{base_url}&role=callee"
            )
        )

        await bot.send_message(
            user.partner_id,
            "📞 **Incoming Call**\n\nClick below to join the call.",
            reply_markup=callee_kb.as_markup(),
            parse_mode="Markdown"
        )

    except Exception as e:
        await message.answer(f"⚠️ Internal error: {e}")
