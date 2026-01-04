import json
import os
from datetime import datetime
import pytz
from config import TIMEZONE, FREE_DAILY_LIMIT

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
PREMIUM_FILE = os.path.join(DATA_DIR, "premium.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

tz = pytz.timezone(TIMEZONE)


def _ensure_files():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    for file in [USERS_FILE, PREMIUM_FILE, HISTORY_FILE]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump({}, f)


_ensure_files()


# ---------- BASIC LOAD / SAVE ----------

def _load(path):
    with open(path, "r") as f:
        return json.load(f)


def _save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ---------- USER SYSTEM ----------

def get_today_key():
    return datetime.now(tz).strftime("%Y-%m-%d")


def register_user(user_id: int):
    users = _load(USERS_FILE)
    uid = str(user_id)

    if uid not in users:
        users[uid] = {
            "used_today": 0,
            "last_date": get_today_key()
        }
        _save(USERS_FILE, users)


def reset_if_new_day(user_id: int):
    users = _load(USERS_FILE)
    uid = str(user_id)
    today = get_today_key()

    if uid in users and users[uid]["last_date"] != today:
        users[uid]["used_today"] = 0
        users[uid]["last_date"] = today
        _save(USERS_FILE, users)


def can_use_video(user_id: int, is_premium: bool):
    users = _load(USERS_FILE)
    uid = str(user_id)

    if is_premium:
        return True

    return users.get(uid, {}).get("used_today", 0) < FREE_DAILY_LIMIT


def increase_usage(user_id: int):
    users = _load(USERS_FILE)
    uid = str(user_id)

    users[uid]["used_today"] += 1
    _save(USERS_FILE, users)


# ---------- PREMIUM SYSTEM ----------

def is_premium(user_id: int):
    premium = _load(PREMIUM_FILE)
    uid = str(user_id)

    if uid not in premium:
        return False

    expiry = premium[uid]
    return datetime.now(tz).timestamp() < expiry


def add_premium(user_id: int, seconds: int):
    premium = _load(PREMIUM_FILE)
    uid = str(user_id)

    premium[uid] = datetime.now(tz).timestamp() + seconds
    _save(PREMIUM_FILE, premium)


def remove_premium(user_id: int):
    premium = _load(PREMIUM_FILE)
    uid = str(user_id)

    if uid in premium:
        del premium[uid]
        _save(PREMIUM_FILE, premium)


# ---------- VIDEO HISTORY (NO REPEAT) ----------

def get_user_history(user_id: int):
    history = _load(HISTORY_FILE)
    return history.get(str(user_id), [])


def add_to_history(user_id: int, video_id: str):
    history = _load(HISTORY_FILE)
    uid = str(user_id)

    history.setdefault(uid, []).append(video_id)
    _save(HISTORY_FILE, history)


def reset_history(user_id: int):
    history = _load(HISTORY_FILE)
    uid = str(user_id)

    history[uid] = []
    _save(HISTORY_FILE, history)