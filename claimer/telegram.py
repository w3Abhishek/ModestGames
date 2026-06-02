import os
import httpx

def get_config():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    return bot_token, chat_id

def send_message(text: str):
    bot_token, chat_id = get_config()
    if not bot_token or not chat_id:
        print("Telegram configuration missing. Skipping message:\n", text)
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        response = httpx.post(url, json=payload, timeout=10.0)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def send_login_prompt(games: list[str]):
    games_text = ", ".join(games) if games else "None"
    
    text = (
        "🎮 <b>Epic Free Games — Login Required</b>\n\n"
        f"Games to claim: <i>{games_text}</i>\n\n"
        "Cookies expired or captcha needed. Click the link below, log in to Epic, "
        "complete any captcha, then extract the cookies.\n\n"
        "👉 https://store.epicgames.com/free-games\n\n"
        "After logging in, run locally:\n"
        "<code>python scripts/export_cookies.py</code>\n"
        "Then update the EPIC_COOKIES secret with the output."
    )
    send_message(text)
