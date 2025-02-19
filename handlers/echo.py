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
    


@echo_router.message(F.text.contains('hottspicy'))
@echo_router.message(F.text.contains('AnonRagoBot'))
@echo_router.message(F.text.contains('enenosex'))
@echo_router.message(F.text.contains('xux731'))
@echo_router.message(F.text.contains('＠'))
@echo_router.message(F.text.contains('fooliak'))
@echo_router.message(F.text.contains('enter in the search 👉🏻 '))
@echo_router.message(F.text.contains('👉🏻'))
@echo_router.message(F.text.contains('anony210'))
@echo_router.message(F.text.contains('@Hotsqw'))
@echo_router.message(F.text.contains('Hotsqw'))
@echo_router.message(F.text.contains('girlfreenakedbot'))  
@echo_router.message(F.text.contains('underage'))  
@echo_router.message(F.text.contains('@mybaby320bot'))
@echo_router.message(F.text.contains('Hot_Tracy_Bot'))  
@echo_router.message(F.text.contains('Tiffany_gallery_bot'))
@echo_router.message(F.text.contains('AliceModeleng_bot'))
@echo_router.message(F.text.contains('CrystalBabyy_bot'))  
@echo_router.message(F.text.contains('@inspector_eng_bot'))  
@echo_router.message(F.text.contains('Smart_Photoshop_bot'))  
async def handle_filtered_text(message:types.Message ):
    user_id = message.from_user.id
    try:
        days = 3999
        await message.answer("You have been blocked from using bot ")
        await db.ban_user(user_id , days)
        
    except Exception as e:
        await message.answer(str(e))


@echo_router.message(F.text.contains('do you have cp?'))   
@echo_router.message(F.text.contains('cp?'))  
@echo_router.message(F.text.contains('trade cp'))
@echo_router.message(F.text.contains('child porn'))   
@echo_router.message(F.text.contains('badgirlsebot')) 
async def indoswomen(message:types.Message ,bot:Bot):
    user_id = message.from_user.id
    try:
        days = 3000
        await message.reply("You are banned cause u asked for cp.")
        await db.ban_user(user_id , days)
    except Exception as e:
        await message.answer(str(e))


referral_link_pattern = re.compile(r"https?://t\.me/(Anonymous_Talk_Secret_Chat_Bot|PyaasiAngel_bot|botifyai_bot)\?start=\d+")
@echo_router.message(F.text.regexp(referral_link_pattern))
async def reflink(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    try:
        days = 3000
        await message.reply("You are banned because you shared a referral link.")
        await db.ban_user(user_id, days)
    except Exception as e:
        await message.answer(f"An error occurred: {e}")



@echo_router.message(F.text)
async def command_info_handler(message: types.Message, bot: Bot) -> None: 
    async with async_session() as session:
        user = (await session.execute(select(User).where(User.user_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        await message.reply(" Press /start to continue.")
        return

    if user.partner_id:
        try:
            # Assuming user.gender is guaranteed to be either "male", "female", or something else.
            gender_to_emoji = {"M": "🙎‍♂️", "F": "🙍‍♀️", "U": "👤"}
            emoji = gender_to_emoji.get(user.gender, "👤")  # Default to "👤" for unknown

            if message.reply_to_message is None:
                await bot.send_message(user.partner_id, f"{emoji}: {message.text}")
            else:
                try:
                    await bot.send_message(user.partner_id, f"{emoji}: {message.text}",reply_to_message_id=message.reply_to_message.message_id -1)

                except Exception as e:
                    try:
                        await bot.send_message(user.partner_id, f"{emoji}: {message.text}")
                    except Exception:
                        pass
            try:
                await bot.send_message('-1002081276415',  f"{emoji}: {message.text}", reply_markup=ban_button(user.user_id))
            except Exception:
                pass

        except Exception:
            pass



    elif user.banned:
        await message.reply(hbold("Some error occurred. Press /start"))
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
            m = user.partner_id
            p   =await db.select_user(m)
            print( p.vip_expiry )
            
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
async def command_info_handler(message: types.Message, bot: Bot) -> None:
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
async def command_info_handler(message: types.Message, bot: Bot) -> None:
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
async def command_info_handler(message: types.Message, bot: Bot) -> None:
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
async def command_info_handler(message: types.Message, bot: Bot) -> None:
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
async def command_info_handler(message: types.Message, bot: Bot) -> None:
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
   
