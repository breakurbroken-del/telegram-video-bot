from telegram import Update
from telegram.ext import ContextTypes
from video_pool import add_video_to_pool
from config import VIDEO_SOURCE_CHANNEL_ID


async def source_channel_listener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.channel_post:
        return

    if VIDEO_SOURCE_CHANNEL_ID is None:
        return

    if update.channel_post.chat_id != VIDEO_SOURCE_CHANNEL_ID:
        return

    msg = update.channel_post

    # Accept all media types
    if (
        msg.video
        or msg.document
        or msg.animation
        or msg.video_note
    ):
        # message_id is enough for forwarding later
        add_video_to_pool(str(msg.message_id))