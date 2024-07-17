from aiogram import Router, F , types , Bot
from aiogram.filters import Command
from database import  user as db
from aiogram.utils.markdown import hbold
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from constant import share_button

from constant import m_ends_chat




admin_router = Router()

ADMINS= 1109490670 ,1460123566, 1428457408 ,1291389760 ,1407808667 ,991914469 ,6567013581 , 6787093249 ,6128599239 ,5624478385



def is_user_admin(user_id):
    return user_id in ADMINS
from aiogram.enums import ParseMode


@admin_router.callback_query(F.data[F.startswith("ban:")][4:].func(int).as_("id"))
async def func(call: types.CallbackQuery, id: int):
    try:
        await db.ban_user(id , 30)
        await call.message.edit_text(f"{id} is banned #ban")
    except Exception as e:
        await call.message.edit_text(f"Some error occured here is error.") 


@admin_router.callback_query(F.data[F.startswith("unban:")][6:].func(int).as_("id"))
async def func(call: types.CallbackQuery, id: int , bot:Bot):
    try:
        await db.unban_user(id)
        await db.make_user_premium(id , 1)
        await bot.send_message(id , "You have been granted 1 day premium access. You can change your partner's gender directly by pressing /setpartnerfemale. Enjoy your VIP access!")
        new_caption = f"#{id} is made VIP for 1 day #unban"
        await bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                caption=new_caption
            )
    except Exception as e:
        print(str(e))
        await call.answer(f"Some error occurred. Here is the error.{str(e)}") 







@admin_router.callback_query(F.data[F.startswith("reject:")][7:].func(int).as_("id"))
async def func(call: types.CallbackQuery, id: int , bot:Bot):
    try:
        await bot.send_message(id , "Your payment was rejected , you can ask for @BotsphereSupport or simply press /cancel. Alternatively, you can try accessing it another way.")
        new_caption = f"#{id} is  #rejected"
        await bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                caption=new_caption
        )
    except Exception as e:
        print(str(e))
        await call.answer(f"Some error occurred. Here is the error.{str(e)}") 









@admin_router.callback_query(F.data[F.startswith("unban:")][6:].func(int).as_("id"))
async def func(call: types.CallbackQuery, id: int, bot: Bot):
    try:
        await db.unban_user(id)
        await db.make_user_premium(id, 1)
        await bot.send_message(
            id, 
            "You have been granted 1 day premium access. You can change your partner's gender directly by pressing /setpartnerfemale. Enjoy your VIP access!"
        )
        await call.message.edit_caption(f"{id} is made VIP for 1 day #unban")
        #await call.message.edit_reply_markup(reply_markup=None)  # Remove the inline buttons
    except Exception as e:
        await call.answer(f"Some error occurred. Here is the error.{str(e)}")



@admin_router.message(Command("ban"))
async def ban_user(message: types.Message, command: Command, bot: Bot):
    if is_user_admin(message.from_user.id) == True:
        try:
            args = command.args
            if not args:
                await message.reply("Give me id to ban")
                return
            args_list = args.split(maxsplit=1)
            culprit = args_list[0]
            days_count = args_list[1] if len(args_list) > 1 else 1

            x = await db.select_user(int(culprit))
            if x:
                await db.ban_user(x.user_id , days_count)
                await message.reply("User banned.")
            else:
                await message.reply("User doesnt exist 404")
        except Exception as e:
            await message.reply(str(e))



@admin_router.message(Command("clearvip"))
async def ban_user(message: types.Message, command: Command, bot: Bot):
    users = await  db.get_all_vip_users()
    for user in users:
        if user.vip_expiry < datetime.now():
            try:
                await bot.send_message(user.user_id ,"Your vip is expired. To buy again contact @BotsphereSupport .")
            except Exception as e:
                await message.answer(str(e))
            await db.remove_user_premium(user.user_id)
            await message.answer(f"{user.user_id} vip removed")


  
@admin_router.message(Command("count"))
async def send_count(message: types.Message):
    # Add more counts as needed
    # For example, let's assume you want counts for different chat_count thresholds
    count10 = await db.get_users_count_with_low_chat_count(10)
    count50 = await db.get_users_count_with_low_chat_count(50)
    count100 = await db.get_users_count_with_low_chat_count(100)
    count200 = await db.get_users_count_with_low_chat_count(200)
    count500 = await db.get_users_count_with_low_chat_count(500)
    count1000 = await db.get_users_count_with_low_chat_count(1000)
    count2000 = await db.get_users_count_with_low_chat_count(2000)
    count3000 = await db.get_users_count_with_low_chat_count(3000)
    count5000 = await db.get_users_count_with_low_chat_count(5000)
    count7500 = await db.get_users_count_with_low_chat_count(7500)
    count10000 = await db.get_users_count_with_low_chat_count(10000)
    count20000 = await db.get_users_count_with_low_chat_count(20000)

    # Create a formatted message
    stats_message = (
        f"Chat Count Statistics 📊\n\n"
        f"10: {count10}\n"
        f"50: {count50}\n"
        f"100: {count100}\n"
        f"200: {count200}\n"
        f"500: {count500}\n"
        f"1000: {count1000}\n"
        f"2000: {count2000}\n"
        f"3000: {count3000}\n"
        f"5000: {count5000}\n"
        f"7500: {count7500}\n"
        f"10000: {count10000}\n"
        f"20000: {count20000}\n"
    )

    # Send the formatted message
    await message.answer(stats_message)

@admin_router.message(Command("d"))
async def user_d(message: types.Message, command: Command, bot: Bot):
    if is_user_admin(message.from_user.id):
        try:
            args = command.args
            if not args:
                await message.reply("Give me id to unban.")
                return

            user = await db.check(int(args))
            if user:
                # Create a formatted message with user information
                m = (
                    f"**User Information**\n\n"
                    f"User ID: `{user.user_id}`\n"
                    f"Premium: `{user.premium}`\n"
                    f"Bonus Count: `{user.bonus_count}`\n"
                    f"Chat Count: `{user.chat_count}`\n"
                    f"Age: `{user.age}`\n"
                    f"Gender: `{user.gender}`\n"
                    f"request: `{user.request}`\n"
                    f"reopen: `{user.reopen}`\n"
                    f"Partner pender: `{user.pgender}`\n"
                    f"Min Age: `{user.min_age}`\n"
                    f"Max Age: `{user.max_age}`\n"
                    f"Lang: `{user.lang}`\n"
                    f"Is Banned: `{user.banned}`\n"
                    f"Previous ID: `{user.previous_id}`\n"
                    f"Banned Expiry: `{user.ban_expiry}`\n"
                    f"Created At: `{user.created_at}`\n\n"
                )
                # Send the formatted message with markdown
                await message.answer(m, parse_mode=ParseMode.MARKDOWN_V2, protect_content=False)
            else:
                await message.reply("User doesn't exist (404).")
        except Exception as e:
            await message.reply(str(e))



@admin_router.message(Command("unban"))
async def ban_user(message: types.Message, command: Command, bot: Bot):
    if is_user_admin(message.from_user.id) == True:
        try:
            args = command.args
            if not args:
                await message.reply("Give me id to unban.")
                return
            args_list = args.split(maxsplit=1)
            culprit = args_list[0]
            x = await db.check(int(culprit))
            if x:
                if x.banned:
                    await db.unban_user(x.user_id)
                    await bot.send_message(x.user_id, "You are unbanned. Please follow the /rules ")
                    await message.reply("User unbanned.")
                else:
                    await message.reply("User is not banned.")
            else:
                await message.reply("User dont exist 404")
        except Exception as e:
            await message.reply(str(e))

@admin_router.message(Command("mv"))
async def ban_user(message: types.Message, command: Command, bot: Bot):
    if is_user_admin(message.from_user.id) == True:
        try:
            args = command.args
            if not args:
                await message.reply("Please provide id.")
                return
            args_list = args.split(maxsplit=1)
            culprit = args_list[0]
            days_count = args_list[1] if len(args_list) > 1 else 30

            x = await db.select_user(int(culprit))
            if x.premium == False:
                try:
                    await db.make_user_premium(x.user_id , int(days_count))
                    await bot.send_message(x.user_id, f"You have been made vip for {days_count} days.")
                    await message.reply("User is been made vip.")
                except Exception as e:
                    await message.answer(f"Error ocurred\n{str(e)}")
            else:
                await message.reply("User is already premium.")
        except Exception as e:
            await message.reply(str(e))



@admin_router.message(Command("rm"))
async def ban_user(message: types.Message, command: Command, bot: Bot):
    if is_user_admin(message.from_user.id) == True:
        try:
            args = command.args
            if not args:
                await message.reply("Please provide id.")
                return
            args_list = args.split(maxsplit=1)
            culprit = args_list[0]
            days_count = args_list[1] if len(args_list) > 1 else 30

            x = await db.select_user(int(culprit))
            if x.premium == True:
                try:
                    await db.remove_user_premium(x.user_id)  
                except Exception as e:
                    await message.answer(f"Error ocurred\n{str(e)}")
            else:
                await message.reply("User is already premium.")
        except Exception as e:
            await message.reply(str(e))



@admin_router.message(Command("cp"))
async def ban_user(message: types.Message, command: Command, bot: Bot):
    if is_user_admin(message.from_user.id) == True:
        try:
            args = command.args
            if not args:
                await message.reply("Please provide id.")
                return
            args_list = args.split(maxsplit=1)
            culprit = args_list[0]
            days_count = args_list[1] if len(args_list) > 1 else 90
            x = await db.select_user(int(culprit))
            if x:
                try:
                    try:
                        await db.delete_match(x.user_id , x.partner_id)
                    except Exception:
                        pass

                    try:
                        await bot.send_message(x.partner_id , m_ends_chat)
                    except Exception:
                        pass

                    try:
                        await db.create_match(x.user_id , message.from_user.id)
                    except Exception:
                        pass

                    await message.reply("You have been matched.")
                except Exception as e:
                    await message.answer(f"Error ocurred\n{str(e)}")
            else:
                await message.reply("User is already premium.")
        except Exception as e:
            await message.reply(str(e))

@admin_router.message(Command("stats"))
async def send_welcome(message: types.Message):
    try:
        all_count  = await db.get_all_count()
        male_count = await db.get_users_count_by_gender('M')
        female_count = await db.get_users_count_by_gender('F')
        premium_count = await db.get_vips_count() 
        banned_count = await db.get_bans_count()
        stats_message = (
            f"User Statistics 📊\n\n"
            f"Total Users: {all_count}\n"
            f"Male Users: {male_count}\n"
            f"Female Users: {female_count}\n"
            f"Premium Users: {premium_count}\n"
            f"Banned Users: {banned_count}\n"
        )
        await message.answer(stats_message)
    except Exception as e:
        await message.answer(f"An error occurred: {e}")




@admin_router.message(Command("bc"))
async def vcheck_user_info(message: types.Message, command: Command, bot: Bot):
    # Check if the command has arguments
    args = command.args
    if not args:
        await message.answer("no args")
        return
    users = await db.get_all_user_ids()
    for user_id in users:
        print(user_id)
        try:
            await bot.send_message(user_id,  f"{args}\nThis message is from admin" ,disable_web_page_preview=True) 
        except Exception:
            pass




@admin_router.message(Command("banbc"))
async def vcheck_user_info(message: types.Message, command: Command, bot: Bot):
    # Check if the command has arguments
    args = command.args
    if not args:
        await message.answer("no args")
        return
    users = await db.get_all_banned_users()
    for user_id in users:
        try:
            await bot.send_message(user_id,  args ,disable_web_page_preview=True) 
        except Exception:
            pass





@admin_router.message(Command("onlym"))
async def vcheck_user_info(message: types.Message, command: Command, bot: Bot):
    # Check if the command has arguments
    args = command.args
    if not args:
        await message.answer("no args")
        return
    users = await db.get_male_users()
    for user_id in users:
        try:
            await bot.send_message(user_id,  f"{args}") 
        except Exception as e:
            print(str(e))


@admin_router.message(Command("onlyv"))
async def vcheck_user_info(message: types.Message, command: Command, bot: Bot):
    # Check if the command has arguments
    args = command.args
    if not args:
        await message.answer("no args")
        return
    users = await db.get_all_male_users()
    for user_id in users:
        try:
            await bot.send_message(user_id,  f"{args}") 
        except Exception as e:
            print(str(e))
            

@admin_router.message(Command("m"))
async def vcheck_user_info(message: types.Message, command: Command, bot: Bot):
    # Check if the command has arguments
    args = command.args
    if not args:
        await message.answer("no args")
        return
    users = await db.get_male_user()
    for user in users:
        try:
            await bot.send_message(user.user_id,  f"{args}\nThis message is from admin" ,disable_web_page_preview=True) 
        except Exception as e:
            print(str(e))



@admin_router.message(Command("banm"))
async def vcheck_user_info(message: types.Message, command: Command, bot: Bot):
    # Check if the command has arguments
    users = await db.get_male_user()
    for user in users:
        try:
            await db.ban_user(user.user_id ,300)
        except Exception as e:
            await message.answer(f"Some error occured.Here is error\n{str(e)}")
    await message.answer("Done.")
       







@admin_router.message(Command("unbanm"))
async def vcheck_user_info(message: types.Message, command: Command, bot: Bot):
    # Check if the command has arguments
    users = await db.get_all_banned_users()
    for user in users:
        try:
            await db.unban_user(user)
        except Exception as e:
            await message.answer(f"Some error occured.Here is error\n{str(e)}")
    await message.answer("Done.")
       









@admin_router.message(Command("v"))
async def vcheck_user_info(message: types.Message, command: Command, bot: Bot):
    # Check if the command has arguments
    args = command.args
    if not args:
        await message.answer("no args")
        return
    users = await db.get_vip_user()
    for user in users:
        try:
            await db.unban_user(user.user_id)
        except Exception as e:
            await message.answer(str(e))
        try:
            await bot.send_message(user.user_id,  f"{args}\nThis message is from admin for only vip users." ,disable_web_page_preview=True) 
        except Exception as e:
            print(str(e))

 
@admin_router.message(Command("del"))
async def ban_user(message: types.Message, command: Command, bot: Bot):
    await db.delete_user(message.from_user.id)
    await message.reply("You are deleted. Thank you.")
     
