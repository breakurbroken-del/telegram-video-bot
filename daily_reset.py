import asyncio
from datetime import datetime, timedelta
import pytz

from storage import _load, _save, USERS_FILE
from config import TIMEZONE, RESET_NOTIFICATION_MESSAGE


tz = pytz.timezone(TIMEZONE)


def _seconds_until_midnight():
    now = datetime.now(tz)
    tomorrow = (now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return (tomorrow - now).total_seconds()


async def daily_reset_task(bot):
    while True:
        # Sleep until 12:00 AM IST
        await asyncio.sleep(_seconds_until_midnight())

        users = _load(USERS_FILE)
        today = datetime.now(tz).strftime("%Y-%m-%d")

        for uid, data in users.items():
            data["used_today"] = 0
            data["last_date"] = today

            # Notify user (ignore failures)
            try:
                await bot.send_message(
                    chat_id=int(uid),
                    text=RESET_NOTIFICATION_MESSAGE
                )
            except:
                pass

        _save(USERS_FILE, users)

        # Safety sleep (avoid double trigger)
        await asyncio.sleep(60)