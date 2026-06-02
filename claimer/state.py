import json
import os

STATE_FILE = "claimed.json"

def _load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def _save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

def is_claimed(offer_id: str) -> bool:
    state = _load_state()
    return offer_id in state

def mark_claimed(offer_id: str, title: str):
    state = _load_state()
    state[offer_id] = title
    _save_state(state)
