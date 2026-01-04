import time

_video_cooldown = {}
_command_cooldown = {}
_silent_block = {}

VIDEO_SPAM_BLOCK = 3600      # 1 hour
CMD_COOLDOWN = 15            # 15 sec


def now():
    return int(time.time())


def is_video_blocked(user_id):
    return _silent_block.get(user_id, 0) > now()


def block_video(user_id):
    _silent_block[user_id] = now() + VIDEO_SPAM_BLOCK


def can_use_video(user_id):
    last = _video_cooldown.get(user_id, 0)
    if now() - last < CMD_COOLDOWN:
        return False
    _video_cooldown[user_id] = now()
    return True


def can_use_command(user_id):
    last = _command_cooldown.get(user_id, 0)
    if now() - last < CMD_COOLDOWN:
        return False
    _command_cooldown[user_id] = now()
    return True