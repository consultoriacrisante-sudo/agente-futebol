import sys

sys.stdout.reconfigure(encoding="utf-8")

import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_FOOTBALL_KEY")

if not api_key:
    print("API Key não encontrada.")
    exit()

url = "https://v3.football.api-sports.io/leagues"

headers = {
    "x-apisports-key": api_key
}

response = requests.get(
    url,
    headers=headers
)

if response.status_code != 200:
    print("Erro ao consultar as ligas.")
    print("Status:", response.status_code)
    print(response.text)
    exit()

data = response.json()

print()
print("LIGAS ENCONTRADAS")
print("=" * 70)

for item in data["response"]:

    liga = item["league"]
    pais = item["country"]

    print(
        f'ID: {liga["id"]} | '
        f'{liga["name"]} | '
        f'País: {pais["name"]}'
    )