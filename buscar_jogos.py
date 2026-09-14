import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from config import CAMPEONATOS

load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")
URL = "https://v3.football.api-sports.io/fixtures"
TIMEZONE_BRASILIA = ZoneInfo("America/Sao_Paulo")


def buscar_jogos():
    if not API_KEY:
        raise RuntimeError("API_FOOTBALL_KEY não configurada.")
    hoje = datetime.now(TIMEZONE_BRASILIA).strftime("%Y-%m-%d")
    print("\nBUSCANDO JOGOS")
    print("=" * 60)
    print(f"Data: {hoje}\n")
    try:
        response = requests.get(
            URL,
            headers={"x-apisports-key": API_KEY},
            params={"date": hoje, "timezone": "America/Sao_Paulo"},
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as erro:
        raise RuntimeError(f"Erro ao consultar API-Football: {erro}") from erro
    return response.json().get("response", [])


def filtrar_jogos(jogos):
    return [jogo for jogo in jogos if jogo.get("league", {}).get("id") in CAMPEONATOS]


def exibir_jogos(jogos):
    print("\nJOGOS DOS CAMPEONATOS MONITORADOS")
    print("=" * 60)
    if not jogos:
        print("Nenhum jogo encontrado para hoje.")
        return
    for jogo in jogos:
        league_id = jogo["league"]["id"]
        campeonato = CAMPEONATOS[league_id]
        data_jogo = datetime.fromisoformat(jogo["fixture"]["date"].replace("Z", "+00:00")).astimezone(TIMEZONE_BRASILIA)
        print(f"\nCompetição: {campeonato['nome']}")
        print(f"Jogo: {jogo['teams']['home']['name']} x {jogo['teams']['away']['name']}")
        print(f"Horário: {data_jogo.strftime('%H:%M')}")
        print("-" * 60)


if __name__ == "__main__":
    filtrados = filtrar_jogos(buscar_jogos())
    print(f"Total monitorado: {len(filtrados)}")
    exibir_jogos(filtrados)
