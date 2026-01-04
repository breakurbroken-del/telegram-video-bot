import os
from dotenv import load_dotenv

load_dotenv()

OWNER_PASSWORD = os.getenv("OWNER_PASSWORD")

# Runtime memory (no DB)
_owner_sessions = set()


def is_owner_authenticated(user_id: int) -> bool:
    return user_id in _owner_sessions


def try_owner_login(user_id: int, password: str) -> bool:
    if password == OWNER_PASSWORD:
        _owner_sessions.add(user_id)
        return True
    return False


def owner_logout(user_id: int):
    _owner_sessions.discard(user_id)