m_is_banned = "You dont have access to bot , press /start to know more"
m_is_not_registered = "You are not registered to register again please press /start again."
m_ends_chat = "Chat Ended\nPress /start to start new chat.\n"
refer_text = "Hey there! I'm inviting you to connect and chat casually with others on Telegram! 👦👧 Join now to make new friends in a friendly environment. Start a conversation anonymously today!"


help_text= """
This bot is used to chat with anonymous users all over the Internet.
Commands:

/start - Start a new chat.
/end - End the current chat.
/stop - Stop searching for a user.
/settings - User settings.
/commands = additional commands.

For assistance, contact @RandomMode_Bot.
To purchase VIP, contact @BotSpheresupport.
"""
vip_features = """
<b>Unlock VIP Benefits!</b>

When you buy a VIP package, you support the bot and get these awesome perks:

💖 <b>Match with Girls</b>
🛡️ <b>Ban Protection</b>

<i>Note: There are no refunds, so make sure you're ready before you buy. Nobody has regretted buying VIP!</i>
"""



rules_text ="""
When using  Bot, please follow these rules:

1. 🔞 No Illegal or NSFW Content.

2. ❗️ No Explicit or Offensive Content.

3. 🗑 No Spam, Promotions, or Scams.

4. 🚨 Report Violations by using /report.

These rules may be updated, and violations can result in actions, including bans. For updates, join our channel: @botsphere"""


buy_vip_notice   = (
    "<b>💳 VIP Payments Update</b>\n"
    "We now process VIP payments through Telegram Star, giving you more payment options. For details, type /vip.\n\n"
    "<b>🥷 Enhanced Anti-Spam</b>\n"
    "New anti-spam measures are in place to keep your experience smooth and secure.\n\n"
    "Stay updated with @Botsphere!"
)


commands_message = """
Available Commands:

- /chat : Start a new chat
- /end: Stop the current chat
- /stop: Stop searching
- /settings: Adjust your settings
- /report: Report a message
- /help: Get bot assistance
- /check : Show user info
"""


donate_message = """
Hey, thank you for considering a donation! 💖 Supporting the Bot server is essential, and your generosity is truly appreciated.

We welcome contributions through various methods:

<strong>For Global Supporters: 🌐</strong>
PayPal: <a href="https://www.paypal.com/paypalme/theRishuPandey">@theRishuPandey</a>
Paypal: <code>@theRishuPandey</code>

<strong>For Indian 🇮🇳 Supporters:</strong>
UPI ID: <code>@randommeet@axl</code>
UPI QR: <a href="https://t.me/RandomMeet/13">Scan QR Code</a>


<strong>For Indonesian 🇮🇩 Supporters:</strong>
QIRIS: <a href="https://t.me/RandomMeet/12">[Click  here for LINK]</a>

<strong>Crypto Enthusiasts:</strong>
Cryptocurrency: 

💰 Toncoin: <code>UQB_UTqa633UG5t6VCK-wEonGzQoBWLRbSS3tJTk8EiO43ts</code>

💰 BTC: <code>1CVzhcHB5Qpfk6h77Er9FSisyfnyYi7oME</code>

Your contribution is most welcome for any other method contact @BotSphereSupport 🚀
"""



from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    WebAppInfo,
)



SUPPORT_URL = "https://t.me/BotsphereSupport"


def buy_unban():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Buy Unban from Admin",  url=SUPPORT_URL)],
        ]
    )
    return kb



def unban_button(data):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Unban + vip",  callback_data=f"unban:{data}")],
            [InlineKeyboardButton(text="Reject",  callback_data=f"reject:{data}")],
        ]
    )
    return kb


def ads_spam(data):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="adspam",  callback_data=f"adspam:{data}")],
        ]
    )
    return kb

def share_button(username, user_id):
    url = f"https://t.me/share/url?url=I invite you to join this best chatting bot.\n\nhttps://t.me/{username}?start={user_id}"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Click to share 🖤", url=url)],
            [InlineKeyboardButton(text="Buy Access using ⭐️", callback_data="access")],
        ]
    )
    return keyboard


def contact_admin():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Contact Admin to donate",  url=SUPPORT_URL)],
        ]
    )
    return kb

def buy_vip():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Buy vip from Admin",  url=SUPPORT_URL)],
        ]
    )
    return kb


def channel_button():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Join channel",  url="https://t.me/botsphere")],
        ]
    )
    return kb


def backup_button():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Join our confession channel",  url="https://t.me/confessPal")],
            [InlineKeyboardButton(text="Similar Chat bots",  url="https://t.me/botsphere/8")],

        ]
    )
    return kb

def ban_button(data):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ban",  callback_data=f"ban:{data}")],
        ]
    )
    return kb



def action_button(user_id  , partner_id , message_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ban", callback_data=f"ban:{partner_id}"),
                InlineKeyboardButton(text="Warn", callback_data=f"warn:{user_id}:{message_id}"),
                InlineKeyboardButton(text="Fake girl ", callback_data=f"fkg:{partner_id}"),


               
            ],
            [   InlineKeyboardButton(text="delete", callback_data=f"delete"),
                InlineKeyboardButton(text="wrong report", callback_data=f"wrong_report:{user_id}")
            ]
        ]
    )
    return kb








def urlm_button(user_id, message_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ban", callback_data=f"bam:{user_id}:{message_id}"),
            InlineKeyboardButton(text="warn", callback_data=f"warn:{user_id}:{message_id}")],
        ]
    )
    return kb












def captcha_button():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Yes",  callback_data="Yes")],
            [InlineKeyboardButton(text="No",  callback_data="no")],
        ]
    )
    return kb


def reopen_button(user_id ):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Yes", callback_data=f"reopened:{user_id}"), InlineKeyboardButton(text="No", callback_data=f"rcancel:{user_id}")]
        ]
    )
    return kb



def start_buttons():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Join channel",  url="https://t.me/botsphere")],
            [InlineKeyboardButton(text="Buy VIP  ",  url=SUPPORT_URL)],
        ]
    )
    return kb



def stop_searching():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Cancel",  callback_data="stop")],
        ]
    )
    return kb

cant_use_bot="""
Hello,

As non-male VIP users, many of you are pressing "skip," which impacts the bot's performance. Additionally, with over 50,000 users, few have joined through referrals.

Here’s the deal: You can only use this bot after I reach 1,000 referrals  in every bot.

What you have to do? just click and join from link additionally you can also earn some airdrop from this.

Tomarket https://t.me/Tomarket_ai_bot/app?startapp=00003e7v

YesCoin https://t.me/theYescoin_bot/Yescoin?startapp=yWyY82

Blum https://t.me/BlumCryptoBot/app?startapp=ref_wYMAcWdPJA

Thank you for your understanding and cooperation.

"""
