import sys

BOT_NAME = sys.argv[2]
BOT_TOKEN = sys.argv[1]

# The public URL sent to users for the WebRTC app
WEB_URL = "https://lovetender.in"

# The internal URL the bot uses to talk to the TeleRTC FastAPI server
# Since both are on the VPS, use localhost to avoid DNS/loopback issues
API_URL = "http://127.0.0.1:8084"
