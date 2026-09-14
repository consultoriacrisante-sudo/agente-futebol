import os
import requests

from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

URL = "https://v3.football.api-sports.io/fixtures"

FIXTURE_ID = 1552733


headers = {
    "x-apisports-key": API_KEY
}

params = {
    "id": FIXTURE_ID
}


response = requests.get(
    URL,
    headers=headers,
    params=params,
    timeout=30
)


print("=" * 60)
print("INSPEÇÃO DO FIXTURE")
print("=" * 60)

print(f"Status HTTP: {response.status_code}")
print()

data = response.json()

print("RESULTADO COMPLETO:")
print("=" * 60)

print(data)
