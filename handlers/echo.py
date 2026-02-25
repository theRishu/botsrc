from aiogram import types, Router, F , Bot
from aiogram.utils.markdown import hbold
from sqlalchemy import select
from database.setup import async_session
from database.model import User , Queue
from database import user as db
from constant import ban_button
from constant import stop_searching
from aiogram.enums.parse_mode import ParseMode
from constant import ban_button ,ads_spam

import re
echo_router = Router()

async def queue(user_id):
    async with async_session() as session:
        return  (await session.execute(select(Queue).where(Queue.user_id == user_id))).scalar_one_or_none()
    



7838980869

# --- Content Filtering Configuration ---

# Level 1: General Spam & Low-Quality Bot Promotion (3999 days ban)
BANNED_KEYWORDS_L1 = [
    'vuxoko', 'AnonRagoBot', 'enenosex', 'xux731', '＠', 'fooliak', 
    'enter in the search 👉🏻 ', '👉🏻', 'anony210', '@Hotsqw', 'Hotsqw', 
    'girlfreenakedbot', 'underage', '@mybaby320bot', 'Hot_Tracy_Bot', 
    'Tiffany_gallery_bot', 'AliceModeleng_bot', 'CrystalBabyy_bot', 
    '@inspector_eng_bot', 'Smart_Photoshop_bot', 'bekakobot', 
    'gezxe44bot', 'gezxe44', 'tplzxe633bot', 'tplzxe633', 'TalkNGoBot'
]

# Level 2: Highly Illegal or Harmful Content (3000 days ban)
BANNED_KEYWORDS_L2 = [
    'do you have cp?', 'cp?', 'trade cp', 'child porn', 'badgirlsebot'
]

# Generic pattern for Telegram bot referral links: t.me/botname?start=... or t.me/botname/app?startapp=...
REFERRAL_PATTERN = re.compile(r"t\.me/([a-zA-Z0-9_]+)(?:/app)?\?start(?:app)?=[a-zA-Z0-9_-]+", re.IGNORECASE)

# --- Consolidated Text Handler ---

@echo_router.message(F.text)
async def handle_all_text(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    text_lower = message.text.lower()
    
    # 1. Check for Level 1 Banned Keywords
    if any(keyword.lower() in text_lower for keyword in BANNED_KEYWORDS_L1):
        await apply_ban(message, user_id, 3999, "🚫 You have been blocked for violating bot rules.")
        return

    # 2. Check for Level 2 Banned Keywords
    if any(keyword.lower() in text_lower for keyword in BANNED_KEYWORDS_L2):
        await apply_ban(message, user_id, 3000, "🚫 You are banned for sharing or asking for prohibited content.")
        return

    # 3. Check for External Referral Links
    match = REFERRAL_PATTERN.search(message.text)
    if match:
        bot_info = await bot.get_me()
        found_bot_username = match.group(1).lower()
        
        # If the referral link is NOT for our own bot, it's a violation
        if found_bot_username != bot_info.username.lower():
            await apply_ban(message, user_id, 3000, "🚫 External referral links are strictly prohibited. You have been banned.")
            return

    # 4. If all checks pass, handle as a regular chat message
    await process_chat_message(message, bot)

async def apply_ban(message: types.Message, user_id: int, days: int, reason: str):
    """Helper to apply a ban and cleanup the message."""
    try:
        await message.reply(hbold(reason))
        await db.ban_user(user_id, days)
        try:
            await message.delete()
        except:
            pass
    except Exception as e:
        print(f"Error applying ban for {user_id}: {e}")

async def process_chat_message(message: types.Message, bot: Bot) -> None: 
    async with async_session() as session:
        user = (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    
    if not user:
        await message.reply("⚠️ You are not registered. Press /start to continue.")
        return

    if user.partner_id:
        try:
            # Emoji indicators for gender
            gender_to_emoji = {"M": "🙎‍♂️", "F": "🙍‍♀️", "U": "👤"}
            emoji = gender_to_emoji.get(user.gender, "👤")

            # Handle replies
            reply_to = None
            if message.reply_to_message:
                # Basic relative reply logic (can be complex in forwarded contexts)
                reply_to = message.reply_to_message.message_id - 1

            try:
                await bot.send_message(
                    chat_id=user.partner_id,
                    text=f"{emoji}: {message.text}",
                    reply_to_message_id=reply_to
                )
            except Exception:
                # Fallback if reply_to_message_id fails
                await bot.send_message(user.partner_id, f"{emoji}: {message.text}")

            # Send to logging group (if exists)
            try:
                await bot.send_message('-1002081276415', f"Log [{user.user_id}]: {message.text}", reply_markup=ban_button(user.user_id))
            except Exception:
                pass

        except Exception as e:
            print(f"Error forwarding message: {e}")
            await message.reply(hbold("❌ Your partner might have blocked the bot or left."))

    elif user.banned:
        await message.reply(hbold("🚫 You are currently banned from using this bot."))
    elif await queue(user.user_id):
        await message.answer(hbold("⏳ Please wait... We are still looking for a partner for you."), reply_markup=stop_searching())
    else:
        await message.reply("💡 You are not in a chat. Type /start to find someone!")

@echo_router.message(F.sticker)
async def handle_sticker(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_sticker(user.partner_id, message.sticker.file_id)
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")



            








@echo_router.message(F.photo)
async def handle_photo(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user =   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return
    
    if  user.gender=='F':
        await bot.send_photo( 1407808667, message.photo[-1].file_id, caption="Click only if this pics is spam" , reply_markup =ads_spam(user.user_id) , protect_content=True)

    if user.chat_count <3 :
        await bot.send_photo( 1291389760, message.photo[-1].file_id, caption="Click only if this pics is spam" , reply_markup =ads_spam(user.user_id) , protect_content=True)


    if user.partner_id:
        try:
            m = user.partner_id
            p = await db.select_user(m)                             

            if p.vip_expiry :
                await bot.send_photo(user.partner_id, message.photo[-1].file_id, caption="Click only if this pics is spam" , reply_markup =ads_spam(user.user_id) , protect_content=True)
            else:
                await bot.send_photo(  user.partner_id, message.photo[-1].file_id, caption=message.caption , protect_content=True )
        except Exception as e:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
            print(str(e))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")


















@echo_router.message(F.animation)
async def handle_animation(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_animation(user.partner_id, message.animation.file_id)
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")





@echo_router.message(F.audio)
async def handle_audio(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_audio(user.partner_id, message.audio.file_id, caption=message.caption  ,  protect_content=True)
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")





@echo_router.message(F.document)
async def handle_document(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_document(user.partner_id, message.document.file_id, caption=message.caption ,  protect_content=True)
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")



@echo_router.message(F.video)
async def handle_video(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_video(user.partner_id, message.video.file_id, caption=message.caption , protect_content=True)
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")



@echo_router.message(F.video_note)
async def handle_video_note(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_video_note(user.partner_id, message.video_note.file_id, protect_content=True)
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")



@echo_router.message(F.voice)
async def handle_voice(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_voice(user.partner_id, message.voice.file_id , protect_content=True)
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")



@echo_router.message(F.location)
async def handle_location(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:

            await bot.send_location(user.partner_id, message.location.latitude  , message.location.longitude, protect_content=True)
        except Exception :
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")


@echo_router.error()
async def error_handler(exception: types.ErrorEvent , bot:Bot):
    await bot.send_message(chat_id=1291389760, text=str(exception.exception))
   
