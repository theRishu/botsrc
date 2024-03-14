from aiogram import Router ,Bot ,types
from aiogram.filters import  Command
from constant  import m_is_banned ,m_is_not_registered , m_ends_chat
from database import user as db
from aiogram.utils.markdown import hbold


end_router = Router()

@end_router.message(Command("end"))
async def end_handler(message:types.Message,bot:Bot) -> None:
    try:    
        user = await db.select_user(message.from_user.id)
        if not user:
            if  await db.is_user_banned(message.from_user.id):
                await message.answer(m_is_banned)
            else:
                await message.answer(m_is_not_registered) 
            return
                
        if user.partner_id != None:
            
            await db.delete_match(user.user_id , user.partner_id)
            try:
                await bot.send_message(user.user_id ,hbold(m_ends_chat))
            except Exception:
                pass
            try:
                await bot.send_message(user.partner_id, hbold(m_ends_chat))
            except Exception:
                pass
        else:
            await message.answer("You are not in chat.\nPress /start to search.")
           
    except Exception as e:
        raise e
   



@end_router.message(Command("setpartnerfemale"))
async def end_handler(message:types.Message,bot:Bot) -> None:
    try:
        user = await db.select_user(message.from_user.id)
        if user.premium==True:
            await db.update_user_pgender(message.from_user.id, "F")
            await message.answer("done")

        else:
            await message.answer("You are not vip")
    except Exception as e:
        await message.answer(str(e) , protect_content=False)
        