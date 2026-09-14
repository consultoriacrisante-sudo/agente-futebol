import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")

if not API_KEY:
    print("BRAVE_SEARCH_API_KEY nao encontrada no .env")
    exit()

url = "https://api.search.brave.com/res/v1/web/search"

headers = {
    "Accept": "application/json",
    "X-Subscription-Token": API_KEY
}

params = {
    "q": "Marseille Strasbourg Ligue 1 onde assistir Brasil",
    "country": "BR",
    "search_lang": "pt-br",
    "count": 10
}

response = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=20
)

print("Status HTTP:", response.status_code)

if response.status_code != 200:
    print(response.text)
    exit()

data = response.json()

resultados = data.get("web", {}).get("results", [])

print("RESULTADOS:", len(resultados))

for resultado in resultados:

    print()
    print("Título:", resultado.get("title"))
    print("URL:", resultado.get("url"))
    print("Descrição:", resultado.get("description"))
