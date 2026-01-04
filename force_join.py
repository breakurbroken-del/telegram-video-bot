from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from config import FORCE_JOIN_CHANNEL_LINK, JOIN_REQUIRED_MESSAGE


async def is_user_joined(bot, user_id: int, channel_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except BadRequest:
        return False


def join_required_keyboard():
    if not FORCE_JOIN_CHANNEL_LINK:
        return None

    button = InlineKeyboardButton(
        text="Join Now ✅",
        url=FORCE_JOIN_CHANNEL_LINK
    )
    return InlineKeyboardMarkup([[button]])