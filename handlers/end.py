from aiogram import Router ,Bot ,types
from aiogram.filters import  Command
from constant  import m_is_banned ,m_is_not_registered , m_ends_chat ,buy_vip_notice
from database import user as db
from aiogram.utils.markdown import hbold
from aiogram.filters import Command
from aiogram import F, types , Router , Bot
from database import user as db
from constant import action_button, m_is_banned , m_is_not_registered ,m_ends_chat
from aiogram.utils.markdown import hbold
from constant import stop_searching
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

end_router = Router()


@end_router.callback_query(F.data[F.startswith("adspam:")][7:].func(int).as_("id"))
async def func(call: types.CallbackQuery, id: int ,bot:Bot):
    try:
        await db.ban_user(id , 3000)
        await bot.send_message(1291389760,  f' {id} was banned by{call.from_user.id')

        await call.delete()
    except Exception as e:
        print(str(e))
        await bot.send_message(1291389760,  str(e))
       
        


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
                if user.gender =="M" and user.premium ==False:
                    await message.answer(buy_vip_notice)
              
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
            await db.can_use(message.from_user.id , True)
            await message.answer("✅ Done! You will now be matched exclusively with girls. Press /start to begin chatting.")
        else:
            await message.answer("You are not vip")
    except Exception as e:
        await message.answer(str(e) , protect_content=False)



@end_router.message(Command("setgender"))
async def end_handler(message:types.Message,bot:Bot) -> None:
    await message.answer(
    "Okay, listen up. This is your last chance to set your gender to male. To confirm, please type /confirmmale. I hope you're smart enough to get it right."
    )

  

@end_router.message(Command("confirmmale"))
async def end_handler(message:types.Message,bot:Bot) -> None:
    try:
        await db.update_user_ugender(message.from_user.id, "M")
        await message.answer("✅ Done! Your gender is set to male.")           
    except Exception as e:
        await message.answer(str(e) , protect_content=False)



@end_router.message(Command("del_by_admin"))
async def ban_user(message: types.Message, command: Command, bot: Bot):
    await db.delete_user(message.from_user.id)
    await message.reply("You are deleted. Thank you.")
     
