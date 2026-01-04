import os
from dotenv import load_dotenv

load_dotenv()

# ====== BASIC SETTINGS ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_PASSWORD = os.getenv("OWNER_PASSWORD")

# ====== LIMIT SETTINGS ======
FREE_DAILY_LIMIT = 30          # free users limit
PREMIUM_DAILY_LIMIT = 999999   # unlimited (logical)

# ====== TIME SETTINGS ======
TIMEZONE = "Asia/Kolkata"
DAILY_RESET_HOUR = 0  # 12:00 AM IST

# ====== CHANNEL SETTINGS ======

# Private channel where videos are stored
VIDEO_SOURCE_CHANNEL_ID = None  # will be set later

# Force join channel (dynamic, owner can change)
FORCE_JOIN_CHANNEL_LINK = None

# ====== MESSAGES (Professional English) ======

START_MESSAGE = (
    "👋 Welcome!\n\n"
    "Use /videos to receive random videos.\n"
    "Daily free limit: 30 videos.\n\n"
    "Upgrade via /subscription for unlimited access."
)

JOIN_REQUIRED_MESSAGE = (
    "🔒 Access Restricted\n\n"
    "You must join our official channel to continue using this bot.\n\n"
    "After joining, return here and use /videos again."
)

LIMIT_REACHED_MESSAGE = (
    "⚠️ Daily Limit Reached\n\n"
    "You have used all 30 free videos for today.\n\n"
    "Upgrade via /subscription to get unlimited access."
)

RESET_NOTIFICATION_MESSAGE = (
    "✅ Your daily video limit has been reset.\n"
    "You can now enjoy more videos."
)

# ====== EMOJI STYLE ======
EMOJI_CHECK = "✅"
EMOJI_LOCK = "🔒"
EMOJI_WARNING = "⚠️"