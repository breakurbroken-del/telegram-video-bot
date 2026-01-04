import os
import json
from datetime import datetime
import pytz

from owner_auth import is_owner_authenticated
from storage import _load, USERS_FILE, PREMIUM_FILE
from config import TIMEZONE

LOG_FILE = "data/bot.log"
tz = pytz.timezone(TIMEZONE)


def _safe_load(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default


def _count_lines(path):
    try:
        with open(path, "r") as f:
            return sum(1 for _ in f)
    except:
        return 0


# ---------------- STATS COMMAND ----------------

async def stats_cmd(update, context):
    user_id = update.effective_user.id
    if not is_owner_authenticated(user_id):
        return

    users = _safe_load(USERS_FILE, {})
    premium = _safe_load(PREMIUM_FILE, {})

    today = datetime.now(tz).strftime("%Y-%m-%d")

    total_users = len(users)
    active_today = sum(1 for u in users.values() if u.get("last_date") == today)
    premium_users = len(premium)

    text = (
        "📊 *Bot Stats*\n\n"
        f"👥 Total users: {total_users}\n"
        f"⚡ Active today: {active_today}\n"
        f"💎 Premium users: {premium_users}\n"
        f"🧾 Log lines: {_count_lines(LOG_FILE)}\n"
    )

    await update.message.reply_text(text, parse_mode="Markdown")


# ---------------- LOGS COMMAND ----------------

async def logs_cmd(update, context):
    user_id = update.effective_user.id
    if not is_owner_authenticated(user_id):
        return

    lines = 20
    if context.args:
        try:
            lines = int(context.args[0])
        except:
            pass

    try:
        with open(LOG_FILE, "r") as f:
            data = f.readlines()[-lines:]
            text = "🧾 *Last Logs*\n\n" + "".join(data)
    except:
        text = "🧾 No logs found."

    await update.message.reply_text(
        f"```{text}```",
        parse_mode="Markdown"
    )