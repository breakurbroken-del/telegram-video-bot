from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.ext import CallbackQueryHandler
from telegram.error import BadRequest

# -------- INTERNAL MODULES --------
from storage import (
    register_user,
    reset_if_new_day,
    can_use_video as can_use_limit,
    increase_usage,
    is_premium,
)

# -------- STATS & LOGS --------
app.add_handler(CommandHandler("stats", stats_cmd))
app.add_handler(CommandHandler("logs", logs_cmd))

from force_join import is_user_joined, join_required_keyboard
from video_pool import pick_random_video
from cooldown import (
    can_use_video,
    can_use_command,
    is_video_blocked,
    block_video,
)

from config import (
    START_MESSAGE,
    LIMIT_REACHED_MESSAGE,
    JOIN_REQUIRED_MESSAGE,
    VIDEO_SOURCE_CHANNEL_ID,
)

# =========================================================
# USER COMMANDS
# =========================================================

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not can_use_command(user_id):
        return
    await update.message.reply_text(START_MESSAGE)


async def videos_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    bot = context.bot

    # ---- HARD SPAM BLOCK (1 hour silent) ----
    if is_video_blocked(user_id):
        return

    # ---- FAST SPAM (15 sec) ----
    if not can_use_video(user_id):
        block_video(user_id)
        return

    # ---- USER REGISTER + RESET ----
    register_user(user_id)
    reset_if_new_day(user_id)

    # ---- FORCE JOIN CHECK ----
    if VIDEO_SOURCE_CHANNEL_ID is not None:
        joined = await is_user_joined(
            bot,
            user_id=user_id,
            channel_id=VIDEO_SOURCE_CHANNEL_ID
        )
        if not joined:
            await update.message.reply_text(
                JOIN_REQUIRED_MESSAGE,
                reply_markup=join_required_keyboard()
            )
            return

    # ---- LIMIT / PREMIUM CHECK ----
    premium = is_premium(user_id)
    if not can_use_limit(user_id, premium):
        await update.message.reply_text(LIMIT_REACHED_MESSAGE)
        return

    # ---- RANDOM VIDEO PICK ----
    message_id = pick_random_video(user_id)
    if not message_id:
        await update.message.reply_text(
            "⚠️ No videos available right now. Please try later."
        )
        return

# -------- BROADCAST --------
app.add_handler(CommandHandler("broadcast", broadcast_cmd))
app.add_handler(CallbackQueryHandler(broadcast_button))

    # ---- FORWARD VIDEO ----
    try:
        await bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=VIDEO_SOURCE_CHANNEL_ID,
            message_id=int(message_id)
        )
        increase_usage(user_id)

    except BadRequest:
        # If one video fails, try next random ONCE
        message_id = pick_random_video(user_id)
        if not message_id:
            return

        await bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=VIDEO_SOURCE_CHANNEL_ID,
            message_id=int(message_id)
        )
        increase_usage(user_id)


async def subscription_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not can_use_command(user_id):
        return

    await update.message.reply_text(
        "💎 Premium Plans\n\n"
        "• 1 Day — ₹2\n"
        "• 1 Week — ₹9\n"
        "• 1 Month — ₹30\n"
        "• 1 Year — ₹300\n\n"
        "To buy premium, please contact support."
    )


async def support_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not can_use_command(user_id):
        return

    await update.message.reply_text(
        "📩 Support\n\n"
        "For premium or help, contact the owner directly."
    )