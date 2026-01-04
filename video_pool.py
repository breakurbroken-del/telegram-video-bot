import json
import os
import random
from storage import get_user_history, add_to_history, reset_history

DATA_DIR = "data"
POOL_FILE = os.path.join(DATA_DIR, "video_pool.json")


def _ensure_pool():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(POOL_FILE):
        with open(POOL_FILE, "w") as f:
            json.dump([], f)


_ensure_pool()


def load_pool():
    with open(POOL_FILE, "r") as f:
        return json.load(f)


def save_pool(videos):
    with open(POOL_FILE, "w") as f:
        json.dump(videos, f, indent=2)


# -------- POOL MANAGEMENT --------

def add_video_to_pool(video_id: str):
    videos = load_pool()
    if video_id not in videos:
        videos.append(video_id)
        save_pool(videos)


def remove_video_from_pool(video_id: str):
    videos = load_pool()
    if video_id in videos:
        videos.remove(video_id)
        save_pool(videos)


# -------- RANDOM PICKER (NO REPEAT) --------

def pick_random_video(user_id: int):
    videos = load_pool()
    if not videos:
        return None

    history = get_user_history(user_id)

    # Available videos = not yet sent to user
    available = [v for v in videos if v not in history]

    # If exhausted, reset cycle
    if not available:
        reset_history(user_id)
        available = videos.copy()

    selected = random.choice(available)
    add_to_history(user_id, selected)
    return selected