import os
import secrets
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = (os.getenv("APP_BASE_URL") or "").rstrip("/")
SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")

if not TOKEN or not BASE_URL:
    raise SystemExit("Configure TELEGRAM_BOT_TOKEN e APP_BASE_URL no .env.")
if not SECRET:
    raise SystemExit("Configure TELEGRAM_WEBHOOK_SECRET no .env (uma string aleatória).")

url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
payload = {
    "url": f"{BASE_URL}/webhook/telegram",
    "secret_token": SECRET,
    "allowed_updates": ["message", "edited_message"],
    "drop_pending_updates": False,
}
response = requests.post(url, json=payload, timeout=20)
print(response.status_code, response.text)
