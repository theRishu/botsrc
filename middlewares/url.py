from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Message, CallbackQuery

from constant import  urlm_button
from database import user as db
from aiogram import Bot

class URLMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
        self.url_group = '-1002231026995'  # Fixed URL group

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Any, data: Dict[str, Any]) -> Any:
        entities = None
        if isinstance(event, Message):
            entities = event.entities
        elif isinstance(event, CallbackQuery) and event.message:
            entities = event.message.entities

        if entities:
            for entity in entities:
                if entity.type in {"url", "text_link"}:
                    await self.bot.send_message(self.url_group, event.text , reply_markup=urlm_button(event.from_user.id ,event.message_id))
                    break
        return await handler(event, data)
