from telegram import Update
from telegram.ext import ContextTypes
from datetime import timedelta

from owner_auth import is_owner_authenticated, try_owner_login
from storage import add_premium, remove_premium
import config

# ---------------- LOGIN ----------------

async def owner_login_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if try_owner_login(update.effective_user.id, text):
        await update.message.reply_text("✅ Owner access granted.")
    else:
        await update.message.reply_text("❌ Wrong password.")


# ---------------- SET SOURCE CHANNEL ----------------

async def set_source_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner_authenticated(update.effective_user.id):
        return

    try:
        channel_id = int(context.args[0])
        config.VIDEO_SOURCE_CHANNEL_ID = channel_id
        await update.message.reply_text(
            f"✅ Source channel ID set to:\n{channel_id}"
        )
    except:
        await update.message.reply_text(
            "❌ Usage:\n/setchannel <CHANNEL_ID>"
        )


# ---------------- SET FORCE JOIN LINK ----------------

async def set_join_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner_authenticated(update.effective_user.id):
        return

    try:
        link = context.args[0]
        config.FORCE_JOIN_CHANNEL_LINK = link
        await update.message.reply_text(
            f"✅ Force-join channel link set:\n{link}"
        )
    except:
        await update.message.reply_text(
            "❌ Usage:\n/setjoin <CHANNEL_LINK>"
        )


# ---------------- SET SUPPORT USERNAME ----------------

async def set_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner_authenticated(update.effective_user.id):
        return

    try:
        username = context.args[0]
        config.START_MESSAGE = config.START_MESSAGE.replace(
            "@YOUR_USERNAME_HERE", username
        )
        await update.message.reply_text(
            f"✅ Support username set to:\n@{username}"
        )
    except:
        await update.message.reply_text(
            "❌ Usage:\n/setsupport <USERNAME>"
        )


# ---------------- PREMIUM COMMANDS ----------------

async def give_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner_authenticated(update.effective_user.id):
        return

    try:
        user_id = int(context.args[0])
        duration = context.args[1].lower()

        seconds_map = {
            "1h": 3600,
            "1d": 86400,
            "1w": 604800,
            "1m": 2592000,
        }

        seconds = seconds_map.get(duration)
        if not seconds:
            raise ValueError

        add_premium(user_id, seconds)
        await update.message.reply_text(
            f"✅ Premium given to {user_id} for {duration}"
        )
    except:
        await update.message.reply_text(
            "❌ Usage:\n/premium <USER_ID> 1h|1d|1w|1m"
        )


async def remove_premium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner_authenticated(update.effective_user.id):
        return

    try:
        user_id = int(context.args[0])
        remove_premium(user_id)
        await update.message.reply_text(
            f"✅ Premium removed from {user_id}"
        )
    except:
        await update.message.reply_text(
            "❌ Usage:\n/removepremium <USER_ID>"
        )