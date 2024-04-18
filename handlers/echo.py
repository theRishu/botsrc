from aiogram import types, Router, F , Bot
from aiogram.utils.markdown import hbold
from sqlalchemy import select
from database.setup import async_session
from database.model import User , Queue
from database import user as db


echo_router = Router()

async def queue(user_id):
    async with async_session() as session:
        return   (await session.execute(select(Queue).where(Queue.user_id == user_id))).scalar_one_or_none()
    

from constant import stop_searching



@echo_router.message(F.text.contains('indoswomen'))
@echo_router.message(F.text.contains('intimues'))
@echo_router.message(F.text.contains('＠'))
@echo_router.message(F.text.contains('IndAnonBot'))
@echo_router.message(F.text.contains('intemx'))
@echo_router.message(F.text.contains('IndoRandomChat_bot'))
@echo_router.message(F.text.contains('Hello.pepolx'))
@echo_router.message(F.text.contains('indanonbot'))
@echo_router.message(F.text.contains('pepolex'))
@echo_router.message(F.text.contains('IndoSecretChat'))
@echo_router.message(F.text.contains('intomasex'))
@echo_router.message(F.text.contains('indAnonBot'))

async  def indoswomen(message:types.Message):
    user_id = message.from_user.id
    try:
        days = 3999
        msg = await message.answer("Look like your id has been hacked.Please clear all session from settings.")
        await db.ban_user(user_id , days)
    except Exception as e:
        await message.answer(str(e))
  


@echo_router.message(F.text.startswith('/'))
async def wrong_cmd(message: types.Message):
    await message.answer("Wrong command. Available commands:\n\n"
                        "/start - Start a new chat.\n"
                         "/next  -to end current and start new .\n"
                         "/end - End the current chat.\n"
                         "/stop - Stop searching for a user.\n"
                         "/settings - User settings.\n"
                         "/commands - Additional commands.")





@echo_router.message(F.text)
async def command_info_handler(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            # Assuming user.gender is guaranteed to be either "male", "female", or something else.
            gender_to_emoji = {"M": "👨", "F": "👩", "U": "👤"}
            emoji = gender_to_emoji.get(user.gender)  # Default to "👤" for unknown
            await bot.send_message(user.partner_id, f"{emoji}: {message.text}")
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."), reply_markup=stop_searching())
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")


@echo_router.message(F.sticker)
async def command_info_handler(message: types.Message, bot: Bot) -> None:
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
async def command_info_handler(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_photo(
            user.partner_id, message.photo[-1].file_id, caption=message.caption
            )
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")



@echo_router.message(F.animation)
async def command_info_handler(message: types.Message, bot: Bot) -> None:
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
async def command_info_handler(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_audio(user.partner_id, message.audio.file_id, caption=message.caption)
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")





@echo_router.message(F.document)
async def command_info_handler(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_document(user.partner_id, message.document.file_id, caption=message.caption)
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")



@echo_router.message(F.video)
async def command_info_handler(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_video(user.partner_id, message.video.file_id, caption=message.caption)
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")



@echo_router.message(F.video_note)
async def command_info_handler(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_video_note(user.partner_id, message.video_note.file_id)
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")



@echo_router.message(F.voice)
async def command_info_handler(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:
            await bot.send_voice(user.partner_id, message.voice.file_id)
        except Exception:
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")



@echo_router.message(F.location)
async def command_info_handler(message: types.Message, bot: Bot) -> None:
    async with async_session() as session:
        user=   (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply("You are not registered. Press /start to register.")
        return

    if user.partner_id:
        try:

            await bot.send_location(user.partner_id, message.location.latitude  , message.location.longitude)
        except Exception :
            await message.reply(hbold("Your partner has blocked the bot. Either wait or skip this chat."))
    elif user.banned:
        await message.reply(hbold("You are banned. Please contact support for assistance."))
    elif await queue(user.user_id):
        await message.answer(hbold("Waiting for someone...."),reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    else:
        await message.reply("You are not currently in a chat. Use /start to find a new chat.")



