from aiogram.filters import Command
from aiogram import types , Router ,F
from database import user as db
from constant import m_is_banned , m_is_not_registered
stop_router = Router()



@stop_router.message(F.text.contains("❌ Cancel"))
@stop_router.message(Command("stop"))
async def command_stop_handler(message:types.Message,) -> None:
    try:    
        user = await db.select_user(message.from_user.id)

        if not user:
            if  await db.is_user_banned(message.from_user.id):
                await message.answer(m_is_banned)
            else:
                await message.answer(m_is_not_registered)  
            return

        if user.request == True:
            await db.make_request_false(user.user_id)
            await message.answer("You have stopped searching for a user.\nPress /start if you want to search again." ,reply_markup=types.ReplyKeyboardRemove(),)
            return
                
        if user.partner_id != None:
            await message.answer("You are already in chat.",reply_markup=types.ReplyKeyboardRemove(),)
            return


      


        if await db.in_search(message.from_user.id) ==True:
            await db.delist_user(message.from_user.id)
            await message.answer("You have stopped searching for a user.\nPress /start if you want to search again." ,reply_markup=types.ReplyKeyboardRemove(),)
        else:
            await message.answer("You were not searching for a user.\nPress /start if you want find someone to chat.",reply_markup=types.ReplyKeyboardRemove(),)
        
    except Exception as e:
        raise e




@stop_router.callback_query(F.data == "stop")
async def command_stop_handler(call:types.CallbackQuery,) -> None:
    try:    
        user = await db.select_user(call.from_user.id)
        if not user:
            if  await db.is_user_banned(call.from_user.id):
                await call.message.edit_text(m_is_banned)
            else:
                await call.message.edit_text(m_is_not_registered)  
            return
        if user.request == True:
            await db.make_request_false(user.user_id)
            await call.message.edit_text("You have stopped searching for a user.\nPress /start if you want to search again." )
            return
                
                
        if user.partner_id != None:
            await call.answer("You are already in chat.")
            return
        if await db.in_search(call.from_user.id) ==True:
            await db.delist_user(call.from_user.id)
            await call.message.edit_text("You have stopped searching for a user.\nPress /start if you want to search again." )
        else:
            await call.message.edit_text("You were not searching for a user.\nPress /start if you want find someone to chat.")
        
    except Exception as e:
        raise e