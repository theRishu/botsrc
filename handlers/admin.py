from aiogram import Router, F , types , Bot
from aiogram.filters import Command
from database import  user as db
from aiogram.utils.markdown import hbold

from constant import SUPPORT_URL

ADMINS= 1109490670 ,1460123566, 1428457408 ,1291389760 ,1407808667 ,991914469

def is_user_admin(user_id):
    return user_id in ADMINS


admin_router = Router()




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
                await message.reply("Give me id to ban")
                return
            args_list = args.split(maxsplit=1)
            culprit = args_list[0]
            days_count = args_list[1] if len(args_list) > 1 else 90

            x = await db.select_user(int(culprit))
            if x.premium:
                try:
                    await db.make_user_premium(x.user_id , days_count)
                except Exception as e:
                    await message.answer(f"Error ocurred\n{str(e)}")

            else:
                await message.reply("User is already premium.")
        except Exception as e:
            await message.reply(str(e))

