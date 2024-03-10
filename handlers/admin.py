from aiogram import Router, F , types , Bot
from aiogram.filters import Command
from database import  user as db
from aiogram.utils.markdown import hbold
from datetime import datetime

admin_router = Router()

ADMINS= 1109490670 ,1460123566, 1428457408 ,1291389760 ,1407808667 ,991914469 ,6567013581 , 6787093249 ,6128599239 ,5624478385

def is_user_admin(user_id):
    return user_id in ADMINS
from aiogram.enums import ParseMode


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
                try:
                    from constant import buy_unban
                    await bot.send_message(x.user_id, f"{hbold('Bot:')} You are banned for {days_count} days for breaking rules. You still can chat until this chat will be over. " , reply_markup=buy_unban() )                       
                except Exception as e:
                    await message.reply(f"Error occurred while sending message to culprit. Here is your error:\n{str(e)}")
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


from constant import m_ends_chat

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
    all_count  = await  db.get_all_count()
    male_count = await db.get_users_count_by_gender('M')
    female_count = await db.get_users_count_by_gender('F')
    premium_count = await db.get_all_vip_users() 
    stats_message = (
        f"User Statistics 📊\n\n"
        f"Total Users: {all_count}\n"
        f"Male Users: {male_count}\n"
        f"Female Users: {female_count}\n"
        f"Premium Users: {premium_count}\n"
    )
    await message.answer(stats_message)



@admin_router.message(Command("jc"))
async def vcheck_user_info(message: types.Message, command: Command, bot: Bot):
    # Check if the command has arguments
    users = await db.get_all_user_ids()
    for user_id in users:
        try:
            await bot.send_message(user_id, "Hey please join our channel @Botsphere.")
        except Exception:
            pass


@admin_router.message(Command("ob"))
async def vcheck_user_info(message: types.Message, command: Command, bot: Bot):
    # Check if the command has arguments
    users = await db.get_all_user_ids()
    for user_id in users:
        try:
            await bot.send_message(user_id,  "Hey, we have many other bots. You can get a list of all bots  using this link  https://t.me/botsphere/8" ,disable_web_page_preview=True)
        except Exception:
            pass


@admin_router.message(Command("bc"))
async def vcheck_user_info(message: types.Message, command: Command, bot: Bot):
    # Check if the command has arguments
    args = command.args
    if not args:
        await message.answer("no args")
        return
    users = await db.get_all_user_ids()
    for user_id in users:
        try:
            await bot.send_message(user_id,  f"{args}\nThis message is from admin" ,disable_web_page_preview=True) 
        except Exception:
            pass




@admin_router.message(Command("del"))
async def ban_user(message: types.Message, command: Command, bot: Bot):
    await db.delete_user(message.from_user.id)
    await message.reply("You are deleted. Thank you.")
     




@admin_router.message(Command("delu"))
async def ban_user(message: types.Message, command: Command, bot: Bot):
    users = await  db.get_all_u_users()
    for user in users:
            await db.delete_user(user.user_id)
            try:
                await bot.send_message("You are not using bot frequently. We are deleting your id from datbase. If you wish to continue you  press /start and join again.")
            except Exception:
                pass
            await message.answer(f"{user.user_id} deleted.")
