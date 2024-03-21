from aiogram.filters import Command
from aiogram import types , Router ,F , Bot
from database import user as db
from aiogram.utils.markdown import hbold

from constant import m_is_banned , m_is_not_registered ,reopen_button ,m_ends_chat
reopen = Router()



@reopen.message(Command("reopen"))
async def command_stop_handler(message:types.Message, bot:Bot) -> None:
    try:    
        user = await db.select_user(message.from_user.id)
        if not user:
            if  await db.is_user_banned(message.from_user.id):
                await message.answer(m_is_banned)
            else:
                await message.answer(m_is_not_registered)  
            return
         
        if user.partner_id != None:
            await message.answer("You are already in chat.",reply_markup=types.ReplyKeyboardRemove(),)
            return

        if await db.in_search(message.from_user.id) ==True:
            await db.delist_user(message.from_user.id)
            return


        if user.request == True:
            await message.answer("You had already requested to open chat. Please wait or press /stop to stop waiting.")
            return



        if user.previous_id !=None:
            p =await db.select_user(user.previous_id)
            if p.reopen ==True:
                await db.make_request_true(user.user_id)
                try:
                    await bot.send_message(p.user_id , "Do you want to reopen chat?" , reply_markup=reopen_button(user.user_id))
                except Exception as e:
                    pass

            await message.answer("Request sent.")

        else:
            await message.answer("Your last request was cancalled. You cant rquest to reopen match")

    except Exception as e:
        raise e

@reopen.callback_query(F.data[F.startswith("reopened:")])
@reopen.callback_query(F.data[F.startswith("rcancel:")])
async def show_gender(call: types.CallbackQuery  , bot:Bot):
    user = await db.select_user(call.from_user.id)
     
    if not user:
        if  await db.is_user_banned(call.from_user.id):
            await message.answer(m_is_banned)
        else:
            await message.answer(m_is_not_registered)  
        return

    components = call.data.split(":")
    func = components[0]
    part = components[1]
    if func =="reopened":

        p = await db.select_user(int(part))

        if p.request == False:
            await  call.message.edit_text("You partner had already cancelled rematch request. Sorry.  ")
            return 

        if p.partner_id != None:
            await  call.message.edit_text("You partner had is already in chat. ")
            return




       
        if user.partner_id:
            try:
                await db.delete_match(user.user_id , user.partner_id)
                await bot.send_message(user.partner_id , m_ends_chat)
            except Exception as e:
                print(str(e)) 
                
            

        await db.delist_user(user.user_id)
        await db.create_match(user_id=call.from_user.id, partner_id=int(part))
        try:
            await bot.send_message(call.from_user.id, hbold("Partner Found!"), reply_markup=types.ReplyKeyboardRemove())
        except Exception as e:
            print(str(e))

        try:
            await bot.send_message(int(part), hbold("Partner Found!"), reply_markup=types.ReplyKeyboardRemove())
        except Exception as e:
            print(str(e))

        await call.message.edit_text("Matched.")
        
       
    
    else:
        await db.remove_previous_id(int(part))
        try:
            await bot.send_message(int(part) , "Your parnter had rejected your reopen request.")
        except  Exception:
            pass

        await call.message.edit_text("You had canceled rematch request.")

