import os
import requests

from dotenv import load_dotenv


# ============================================================
# CONFIGURAÇÃO
# ============================================================

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

URL = "https://v3.football.api-sports.io/fixtures/lineups"


# ============================================================
# BUSCAR ESCALAÇÕES
# ============================================================

def buscar_lineups(fixture_id):

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "fixture": fixture_id
    }

    print()
    print("URL:")
    print(URL)

    print()
    print("PARAMETROS:")
    print(params)

    print()
    print("CONSULTANDO API...")
    print("-" * 60)

    response = requests.get(
        URL,
        headers=headers,
        params=params,
        timeout=30
    )

    print(f"HTTP STATUS: {response.status_code}")

    print()
    print("RESPOSTA BRUTA DA API")
    print("-" * 60)

    print(response.text)

    if response.status_code != 200:

        print()
        print("ERRO HTTP")

        return []

    try:

        data = response.json()

    except Exception as erro:

        print()
        print("ERRO AO CONVERTER JSON:")
        print(erro)

        return []

    print()
    print("ERROS DA API")
    print("-" * 60)

    print(data.get("errors"))

    print()
    print("RESULTS")
    print("-" * 60)

    print(data.get("results"))

    print()
    print("TOTAL DE TIMES:")
    print(len(data.get("response", [])))

    return data.get("response", [])
