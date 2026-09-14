import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise SystemExit("Configure TELEGRAM_BOT_TOKEN no .env.")
response = requests.post(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook", json={"drop_pending_updates": False}, timeout=20)
print(response.status_code, response.text)
