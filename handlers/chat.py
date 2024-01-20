from aiogram.filters import Command
from aiogram import F, types , Router , Bot
from database import user as db
from constant import m_is_banned , m_is_not_registered
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



chat_router = Router()

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

@chat_router.message(Command("chat"))
async def command_start_handler(message:types.Message,bot:Bot) -> None:
    try:    
        user = await db.select_user(message.from_user.id)
        if not user:
            if  await db.is_user_banned(message.from_user.id):
                await message.answer(m_is_banned)
            else:
                await message.answer(m_is_not_registered) 
            return
                
        if user.partner_id != None:
            await message.answer("You are already in chat.",reply_markup=types.ReplyKeyboardRemove())
            return
            
        if await db.in_search(message.from_user.id)==True:
            await message.reply("You are already searching for user.")
           
        else:

            if user.gender  == 'U':
                await message.reply("To use this bot you need to setup your gender.")
                await message.answer("Select your gender.", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[BUTTON_UMALE,BUTTON_UFEMALE ,BUTTON_BACK],
                resize_keyboard=True ))
                await message.answer("After selecting your gender you can continue chatting by pressing /chat")

                return


            if user.chat_count %10 ==9:
                await message.answer("Please follow the /rules, and don't forget to join @Botsphere.")
            
            else:
                pass


            await db.enlist_user(message.from_user.id)
            match = await db.get_match(user.user_id, user.gender, user.pgender , user.previous_id)
            if match != None:
                await db.delist_user(message.from_user.id)
                await db.delist_user(match)
                await db.create_match(user_id = message.from_user.id , partner_id = match)
                try:
                    await bot.send_message( message.from_user.id , hbold("Partner Found!"),reply_markup=types.ReplyKeyboardRemove())
                except Exception:
                    pass
                try:
                    await bot.send_message( match,hbold("Partner Found!"),reply_markup=types.ReplyKeyboardRemove())
                except Exception:
                    pass
            else:
                await message.answer(
                    hbold("Waiting for someone...."),
                      reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    except Exception as e:
        raise e
   






@chat_router.message(F.text.contains("💬"))
async def command_start_handler(message:types.Message,bot:Bot) -> None:
    try:    
        user = await db.select_user(message.from_user.id)
        if not user:
            if  await db.is_user_banned(message.from_user.id):
                await message.answer(m_is_banned)
            else:
                await message.answer(m_is_not_registered) 
            return
                
        if user.partner_id != None:
            await message.answer("You are already in chat.",reply_markup=types.ReplyKeyboardRemove())
            return
            
        if await db.in_search(message.from_user.id)==True:
            await message.reply("You are already searching for user.")
        else:
            await db.enlist_user(message.from_user.id)
            match = await db.get_match(user.user_id, user.gender, user.pgender , user.previous_id)
            if match != None:
                await db.delist_user(message.from_user.id)
                await db.delist_user(match)
                await db.create_match(user_id = message.from_user.id , partner_id = match)
                try:
                    await bot.send_message(message.from_user.id , hbold("Partner Found!"),reply_markup=types.ReplyKeyboardRemove())
                except Exception:
                    pass
                try:
                    await bot.send_message(match , hbold("You've matched with a user who's new to this bot. Please be welcoming! "),reply_markup=types.ReplyKeyboardRemove())
                except Exception:
                    pass
            else:
                await message.answer(
                    hbold("Waiting for someone...."),
                      reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="❌ Cancel")]], resize_keyboard=True))
             
    except Exception as e:
        raise e
   
