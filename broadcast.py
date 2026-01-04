from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes
from owner_auth import is_owner_authenticated
from storage import _load, USERS_FILE

# runtime memory
_pending_broadcast = {}


def _get_all_users():
    users = _load(USERS_FILE)
    return [int(uid) for uid in users.keys()]


# ---------------- START BROADCAST ----------------
async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_owner_authenticated(user_id):
        return

    # CASE 1: text broadcast
    if update.message.text and context.args:
        text = " ".join(context.args)
        _pending_broadcast[user_id] = {
            "type": "text",
            "text": text
        }

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Confirm", callback_data="bc_confirm"),
                InlineKeyboardButton("❌ Cancel", callback_data="bc_cancel"),
            ]
        ])

        await update.message.reply_text(
            f"📢 *Broadcast Preview*\n\n{text}",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        return

    # CASE 2: media broadcast (reply)
    if update.message.reply_to_message:
        msg = update.message.reply_to_message

        payload = {"type": None}

        if msg.photo:
            payload["type"] = "photo"
            payload["file_id"] = msg.photo[-1].file_id
            payload["caption"] = msg.caption or ""

        elif msg.video:
            payload["type"] = "video"
            payload["file_id"] = msg.video.file_id
            payload["caption"] = msg.caption or ""

        if payload["type"]:
            _pending_broadcast[user_id] = payload

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Confirm", callback_data="bc_confirm"),
                    InlineKeyboardButton("❌ Cancel", callback_data="bc_cancel"),
                ]
            ])

            await update.message.reply_text(
                "📢 *Broadcast Preview*\n\nConfirm to send this media to all users.",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            return

    await update.message.reply_text(
        "❌ Usage:\n"
        "/broadcast <text>\n\n"
        "OR reply to an image/video with:\n"
        "/broadcast"
    )


# ---------------- BUTTON HANDLER ----------------
async def broadcast_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if not is_owner_authenticated(user_id):
        await query.answer("Not allowed", show_alert=True)
        return

    if user_id not in _pending_broadcast:
        await query.answer("No broadcast found")
        return

    data = query.data
    payload = _pending_broadcast[user_id]

    if data == "bc_cancel":
        del _pending_broadcast[user_id]
        await query.edit_message_text("❌ Broadcast cancelled.")
        return

    if data == "bc_confirm":
        users = _get_all_users()
        sent = 0

        for uid in users:
            try:
                if payload["type"] == "text":
                    await context.bot.send_message(uid, payload["text"])

                elif payload["type"] == "photo":
                    await context.bot.send_photo(
                        uid,
                        payload["file_id"],
                        caption=payload.get("caption", "")
                    )

                elif payload["type"] == "video":
                    await context.bot.send_video(
                        uid,
                        payload["file_id"],
                        caption=payload.get("caption", "")
                    )

                sent += 1
            except:
                pass

        del _pending_broadcast[user_id]

        await query.edit_message_text(
            f"✅ Broadcast sent to {sent} users."
        )