import datetime
from typing import Optional
from aiogram import Router , types , Bot
from aiogram.filters import CommandStart , CommandObject , Command
from constant import start_buttons
from database import user as db
from aiogram.utils.markdown import hbold
from constant import stop_searching , channel_button , share_button ,backup_button ,unban_button ,vip_features
from aiogram.types import LabeledPrice, PreCheckoutQuery

start_router = Router()

from aiogram import F
from aiogram import types

from config import BOT_NAME



BUTTON_UFEMALE = types.InlineKeyboardButton(text="Female ♀️", callback_data="FFF"),
BUTTON_UMALE = types.InlineKeyboardButton(text="Male ♂️", callback_data="MMM"),


@start_router.message(CommandStart(deep_link=True))
async def handler(message: types.Message, command: CommandObject):
    ref = command.args
    user = await db.check(message.from_user.id)
    if not user:
        if ref and ref.isdigit() and await db.is_user_present(int(ref)):
            await db.update_bonus_count(int(ref))

        await message.answer("To use this bot, you need to set up your gender. Please Select your gender.", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[BUTTON_UMALE, BUTTON_UFEMALE],resize_keyboard=True))
        await db.add_user(message.from_user.id  , "U")
    else:
        await message.answer("Please press /start to chat.")


@start_router.message(CommandStart())
async def command_start_handler(message: types.Message, bot: Bot) -> None:
    user = await db.select_user(message.from_user.id)
    if user:
        if user.gender == "U":
            await message.answer("To use this bot, you need to set up your gender. Please Select your gender.", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[BUTTON_UMALE, BUTTON_UFEMALE],resize_keyboard=True))
            return
        if user.request == True:
            await message.answer("You are waiting so your previous partner can match with you again. If You want to match  new partner You can press /stop and find new one." , reply_markup=stop_searching())
            return
        if user.partner_id:
            await message.answer("You are already in a chat.", reply_markup=types.ReplyKeyboardRemove())
            return
        if await db.in_search(message.from_user.id):
            await message.reply("You are already searching for a user. Please wait." ,reply_markup=stop_searching())
            return

        if user.chat_count % 10 == 9:
            await message.answer("Please follow the /rules, and don't forget to join @Botsphere.")

        elif user.chat_count > 50:
            result = await bot.get_chat_member("@Botsphere", user.user_id)
            if result.status not  in ["member", "creator", "administrator"]:
                await message.answer("To use this bot further , You need to join @Botsphere." , reply_markup=channel_button())
                return 
        else:
            pass

        await db.enlist_user(message.from_user.id)
        match = await db.get_match(user.user_id, user.gender, user.pgender, user.previous_id)

        if match:
            await db.delist_user(message.from_user.id)
            await db.delist_user(match)
            await db.create_match(user_id=message.from_user.id, partner_id=match)
            try:
                await bot.send_message(message.from_user.id, hbold("Partner Found!"), reply_markup=backup_button())
            except Exception as e:
                print(str(e))
            try:
                await bot.send_message(match, hbold("Partner Found!"), reply_markup=backup_button())
            except Exception as e:
                print(str(e))
        else:
            await message.answer("🚀 Start looking for a partner for you..." , reply_markup=stop_searching())

    else:
        botname = await bot.get_me()

        if await db.is_user_banned(message.from_user.id):
            x = await  db.check(message.from_user.id)
            if x.bonus_count >=3:
                await db.consume_bonus_count(x.user_id) 
                await db.unban_user(message.from_user.id)
                await message.answer("You have sucessfully invited 3 people. Now you can use this bot.\n Next step, you need to set up your gender first. Press the button below ",  reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[BUTTON_UMALE ,BUTTON_UFEMALE]))

            else:

                await message.answer(f"""
<b>⚠️ You need to invite 3 people to use this Bot ⭐️</b>

You've referred {x.bonus_count} person(s)
🔗 Your Link: <code> https://t.me/{botname.username}?start={message.from_user.id}</code>

Note : You can also buy access using  17 telegram stars.""",

reply_markup=share_button(botname.username , message.from_user.id))
        else:
            await message.answer(f"<b> Welcome to @{botname.username}</b>!\n\nThanks for starting the bot. Next step, you need to set up your gender first. Press the button below 👇",reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[BUTTON_UMALE ,BUTTON_UFEMALE],resize_keyboard=True))

@start_router.callback_query(F.data.in_(["MMM", "FFF"]))
async def show_gender(call: types.CallbackQuery):
    gender = "M" if call.data == "MMM" else "F" if call.data == "FFF" else None
    user_id = call.from_user.id
    try:
        await db.add_user(user_id ,gender)
        await call.message.edit_text("Everything is set. Now press /start to search user.")

    except Exception as e:
        print(str(e))
        await db.update_user_ugender(user_id ,gender)
        await call.message.edit_text("Everything is set. Now press /start to search user.")







@start_router.callback_query(F.data == "access")
async def show_gender(call: types.CallbackQuery , bot:Bot):
    await call.message.delete()
    await bot.send_invoice(
        chat_id=call.from_user.id,
        provider_token="",
        title="Buy access",
        description = "You are about to purchase access. With this purchase, you will also receive VIP access for 1 day.",
        payload="payload",
        currency="XTR",  # XTR only, don't change
        prices=[
            LabeledPrice(label="label", amount=17),  # 5 telegram stars
        ],
    )


@start_router.message(Command("buy_access"))
async def show_gender(msg: types.Message , bot:Bot):
    if await db.is_user_banned(msg.from_user.id):
        await bot.send_invoice(
        chat_id=msg.from_user.id,
        provider_token="",
        title="Buy access",
        description = (
            "🎉 Don't miss out! This offer is available for just 2 days. Grab it now and enjoy VIP benefits for 2 days! 🎉\n\n"
            "Prefer not to use a star? No problem! You can buy access using UPI. Just press /upi_access to find out more."),
        payload = "payload",
        currency="XTR",  # XTR only, don't change
        prices=[
            LabeledPrice(label="label", amount=5),  # 5 telegram stars
        ],
    )
    else:
        await msg.answer("This is nost for you.Try /buy_vip instead")





@start_router.message(Command("vip"))
@start_router.message(Command("buy_vip"))
async def show_gender(msg: types.Message , bot:Bot):
    await msg.answer(vip_features)
    await bot.send_invoice(
        chat_id=msg.from_user.id,
        provider_token="",
        title="Buy vip",
        description = "VIP for 1 month.",
        payload="payload",
        currency="XTR",  # XTR only, don't change
        prices=[
            LabeledPrice(label="label", amount=200),  # 5 telegram stars
        ],
    )


@start_router.pre_checkout_query()
async def checkout_handler(checkout_query: PreCheckoutQuery):
    await checkout_query.answer(ok=True)

@start_router.message(F.successful_payment)
async def handle_successful_payment(msg: types.Message, bot: Bot):
    try:
        user_id = msg.from_user.id
        payment_charge_id = msg.successful_payment.telegram_payment_charge_id
        total_amount = msg.successful_payment.total_amount
        # Process refund if necessary
        #await bot.refund_star_payment(user_id, payment_charge_id)

        # Handle payment based on the amount
        if total_amount == 5 :
            # Unban user and grant 1-day premium access
            await db.unban_user(user_id)
            await db.make_user_premium(user_id, 2)
            await msg.answer(f"Your transaction ID: {payment_charge_id}. Payment of {total_amount} successful!" , protect_content=False)
            await msg.answer("You have been granted 1 day premium access. You can change your partner's gender directly by pressing /setpartnerfemale. Enjoy your VIP access!")
        
        if  total_amount ==17 :
            # Unban user and grant 1-day premium access
            await db.unban_user(user_id)
            await db.make_user_premium(user_id, 1)
            await msg.answer(f"Your transaction ID: {payment_charge_id}. Payment of {total_amount} successful!" , protect_content=False)
            await msg.answer("You have been granted 1 day premium access. You can change your partner's gender directly by pressing /setpartnerfemale. Enjoy your VIP access!")


        elif total_amount == 200:
            # Grant 300-day premium access
            await db.make_user_premium(user_id, 30)
            await msg.answer(f"Your transaction ID: {payment_charge_id}. Payment of {total_amount} successful!"  , protect_content=False)
            await msg.answer("You have been granted 30 day premium access. You can change your partner's gender directly by pressing /setpartnerfemale. Enjoy your VIP access!")


        # Log transaction in the database
        await bot.send_message(
            chat_id=1291389760,
            text=f"New #transaction logged:\nUser ID: {user_id}\nTransaction ID: {payment_charge_id}\nAmount: {total_amount}"
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        await msg.answer("An error occurred while processing your payment. Please contact support.")
       











from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup




class Form(StatesGroup):
    start = State()
    sent = State()





@start_router.message(Command("upi_access"))
async def show_gender(msg: types.Message , bot:Bot,state: FSMContext):
    if await db.is_user_banned(msg.from_user.id):
        await msg.answer("To purchase  access , please make a payment of 15 rupees to UPI ID: <code> randommeet@axl</code>")
        await msg.answer("By purchasing  you will get 1 day vip for free.")
        await msg.answer("After paying please send me screenshot so we can confirm.")
        await state.set_state(Form.start)
    else:
        await msg.answer("This is not for you.Try /buy_vip instead")


# State handler for the confession state
@start_router.message(Form.start)
async def handle_confession(message: types.Message, state: FSMContext  , bot:Bot) -> None:
    if message.content_type == 'photo':
        await bot.send_photo(1291389760, message.photo[-1].file_id, caption=f"#{str(message.from_user.id)}",  reply_markup=unban_button(message.from_user.id))
        await message.answer("Sent to admin. Please wait")
        await state.set_state(Form.sent)
    else:
        await message.answer("Please send me screenshot of payment here. Dont send compressed file. 15 rupees to UPI ID: <code> randommeet@axl</code> ")



@start_router.message(Command("done"))
async  def  handle_confession(message: types.Message, state: FSMContext  , bot:Bot) -> None:
    if await state.get_state() == Form.sent:
        await message.answer("Cleard.")
        await state.clear()
    else:
        await message.answer("You are not in state. to buy access press /buy_access")

@start_router.message(Form.sent)
async  def  handle_confession(message: types.Message, state: FSMContext  , bot:Bot) -> None:
    await message.answer("Please wait the admin will check and you will get access.If you want to stop this you can press /don")

