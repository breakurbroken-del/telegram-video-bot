import os
from dotenv import load_dotenv

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# -------- INTERNAL IMPORTS --------

from handlers import (
    start_cmd,
    videos_cmd,
    subscription_cmd,
    support_cmd,
)

from owner_commands import (
    owner_login_cmd,
    set_source_channel,
    set_join_link,
    set_support,
    give_premium,
    remove_premium_cmd,
)

from broadcast import (
    broadcast_cmd,
    broadcast_button,
)

from stats import (
    stats_cmd,
    logs_cmd,
)

from channel_listener import source_channel_listener
from daily_reset import daily_reset_task

# -------- ENV --------

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # =========================================================
    # USER COMMANDS
    # =========================================================
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("videos", videos_cmd))
    app.add_handler(CommandHandler("subscription", subscription_cmd))
    app.add_handler(CommandHandler("support", support_cmd))

    # =========================================================
    # OWNER LOGIN (PASSWORD MESSAGE)
    # =========================================================
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, owner_login_cmd)
    )

    # =========================================================
    # OWNER COMMANDS
    # =========================================================
    app.add_handler(CommandHandler("setchannel", set_source_channel))
    app.add_handler(CommandHandler("setjoin", set_join_link))
    app.add_handler(CommandHandler("setsupport", set_support))
    app.add_handler(CommandHandler("premium", give_premium))
    app.add_handler(CommandHandler("removepremium", remove_premium_cmd))

    # =========================================================
    # BROADCAST SYSTEM
    # =========================================================
    app.add_handler(CommandHandler("broadcast", broadcast_cmd))
    app.add_handler(CallbackQueryHandler(broadcast_button))

    # =========================================================
    # STATS & LOGS
    # =========================================================
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("logs", logs_cmd))

    # =========================================================
    # SOURCE CHANNEL LISTENER (AUTO VIDEO POOL)
    # =========================================================
    app.add_handler(
        MessageHandler(filters.ChatType.CHANNEL, source_channel_listener)
    )

    # =========================================================
    # DAILY RESET TASK (12:00 AM IST)
    # =========================================================
    app.job_queue.run_once(
        lambda ctx: ctx.application.create_task(
            daily_reset_task(ctx.application.bot)
        ),
        when=1
    )

    # =========================================================
    # START BOT
    # =========================================================
    app.run_polling()


if __name__ == "__main__":
    main()