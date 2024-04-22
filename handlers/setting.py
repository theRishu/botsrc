from aiogram import Router , types , F , Bot
from aiogram.filters import Command
from constant import m_is_not_registered

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

BUTTON_GENDER  = InlineKeyboardButton(text="👨Gender 👩", callback_data="ugender"),
BUTTON_PGENDER  = InlineKeyboardButton(text=" Gender Preference", callback_data="pgender"),
BUTTON_MEDIA  = InlineKeyboardButton(text="🔙 Media", callback_data="media"),
BUTTON_VIP = InlineKeyboardButton(text=" 🌟 VIP", callback_data="vip"),
BUTTON_BACK = InlineKeyboardButton(text="🔙 Back", callback_data="back"),

BUTTON_UMALE = InlineKeyboardButton(text="Male 👨", callback_data="umale"),
BUTTON_UFEMALE = InlineKeyboardButton(text="Female 👩", callback_data="ufemale"),
BUTTON_UUNKNOWN = InlineKeyboardButton(text="Unknown 👤", callback_data="unone"),


BUTTON_PMALE = InlineKeyboardButton(text="Male 👨", callback_data="pmale"),
BUTTON_PFEMALE = InlineKeyboardButton(text="Female 👩", callback_data="pfemale"),
BUTTON_PUNKNOWN = InlineKeyboardButton(text="Both👨👩 ", callback_data="pnone"),


from database import user as db

setting_router = Router()



@setting_router.message(Command("setting"))
@setting_router.message(Command("settings"))
async def setting_handler(message: Message):
    try:
        user = await db.select_user(message.from_user.id)
        if not user:
            await message.answer(m_is_not_registered)
            return
        
        if user.bonus_count >= 3:
            await db.make_user_premium(user.user_id , 5)
            await db.consume_bonus_count(user.user_id)
            await message.answer("Wow you have been made vip for 5 days. Enjoy Press /settings to continue.")
        else:
            await message.answer("Settings: ⚙️", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[BUTTON_GENDER,
                                 BUTTON_PGENDER,
                                 BUTTON_VIP],
                resize_keyboard=True,
            ))
        
    except Exception as e:
        await message.answer(f"Some error contact admin. Here is error {str(e)}")

from aiogram.fsm.context import FSMContext



@setting_router.callback_query(F.data == "ugender")
async def show_gender(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text("Settings", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[BUTTON_UMALE,BUTTON_UFEMALE ,
                                 BUTTON_BACK],
                resize_keyboard=True,
            ))
    except Exception as e:
        await call.answer(f"Some error occured contact admins  here is error {str(e)}")




@setting_router.callback_query(F.data == "umale")
@setting_router.callback_query(F.data == "ufemale")
@setting_router.callback_query(F.data == "unone")
async def show_gender(call: CallbackQuery, state: FSMContext):
    try:
        if call.data == "umale":
            data = "M"
        elif call.data == "ufemale":
            data = "F"
        else:
            data = "U"

        await db.update_user_ugender(call.from_user.id, data)
        await call.answer("Gender Selected", show_alert=True)

    except Exception as e:
        await call.message.edit_text(f"Some error occcured press /start to continue or contact admin.\nHere is erro {str(e)}")




@setting_router.callback_query(F.data == "pgender")
async def show_gender(call: CallbackQuery, state: FSMContext , bot:Bot):
    try:
        user = await db.select_user(call.from_user.id)
        if user.premium ==True:
            await call.message.edit_text(
                "Select your partner gender.", 
                reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[BUTTON_PMALE,BUTTON_PFEMALE ,BUTTON_PUNKNOWN,
                                 BUTTON_BACK],
                resize_keyboard=True))
        else:
            await call.message.edit_text("Only VIP user can select partner gender. You can see how to get vip in vip section of /settings.",  protect_content=False)
    except Exception as e:
        await call.message.edit_text(f"Some error occured contact admins  here is error {str(e)}" , protect_content=False)



@setting_router.callback_query(F.data == "pmale")
@setting_router.callback_query(F.data == "pfemale")
@setting_router.callback_query(F.data == "pnone")
async def show_gender(call: CallbackQuery, state: FSMContext):
    try:
        if call.data == "pmale":
            data = "M"
        elif call.data == "pfemale":
            data = "F"
        else:
            data = "U"

        await db.update_user_pgender(call.from_user.id, data)
        await call.answer("Partner Gender Selected", show_alert=True)

    except Exception as e:
        await call.message.edit_text(f"Some error occcured press /start to continue or contact admin.\nHere is erro {str(e)}")

       





VIP_TEXT ="""
Unlock VIP Privileges in 2 Simple Ways:

1) Invite Friends:
   - Obtain a  5-day VIP license by inviting 3 new users through your referral link. 
   - Invite a minimum of 3 users to get VIP benefits.

2) Purchase VIP:
   - For Global Users: 💵 $4 
   - For Indian Users: 🇮🇳 ₹300
   - For Indo Users: 🇮🇩 Rp 50.000
   Duration: 30 days.

To buy VIP, just message @BotsphereSupport !
"""

from constant import SUPPORT_URL

def vip_keyboard(tg_referral_url, wa_referral_url):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Buy VIP ",  url=SUPPORT_URL)],
            [InlineKeyboardButton(text="Invite via Telegram", url=tg_referral_url)],
            [InlineKeyboardButton(text="Invite via WhatsApp", url=wa_referral_url)],
            [InlineKeyboardButton(text="🔙 Back", callback_data="back")]
        ]
    )
    return kb


from constant import refer_text
@setting_router.callback_query(F.data == "vip")
async def show_gender(call: CallbackQuery, state: FSMContext , bot:Bot):
    try:
        user = await db.select_user(call.from_user.id)
        if user.premium ==True:
            await call.message.answer(f"You are already vip. You vip will expire on {user.vip_expiry_date}")
        else:
            bot = await bot.get_me()
            tg_referral_url = f"https://t.me/share/url?url=https://t.me/{bot.username}?start={user.user_id}&text={refer_text}"
            wa_referral_url = f"https://api.whatsapp.com/send?text={refer_text}+https://{bot.username}.t.me?start={user.user_id}"
            await call.message.edit_text(
                VIP_TEXT,
                reply_markup=vip_keyboard(tg_referral_url ,wa_referral_url)
            )
    except Exception as e:
        await call.answer(f"Some error occured contact admins  here is error {str(e)}")





@setting_router.callback_query(F.data == "back")
async def show_gender(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text("Settings ;⚙️", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[BUTTON_GENDER,
                                 BUTTON_PGENDER,
                                 BUTTON_VIP],
                resize_keyboard=True,
            ))
    except Exception as e:
        await call.answer(f"Some error occured contact admins  here is error {str(e)}")



from aiogram.enums import ParseMode


@setting_router.message(Command(commands=["check", "checks"]))
async def show_help(message: Message, bot: Bot) -> None:
    user = await db.check(message.from_user.id)
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
        f"can user: `{user.can_use}`\n"
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
    await message.answer(m, parse_mode=ParseMode.MARKDOWN_V2 , protect_content=False)