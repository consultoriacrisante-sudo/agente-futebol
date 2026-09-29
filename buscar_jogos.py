import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from config import CAMPEONATOS, INCLUIR_JOGOS_SELECOES

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


def _eh_selecao(jogo):
    """Identifica partidas de seleções sem depender de IDs fixos de torneios."""
    times = jogo.get("teams") or {}
    casa = times.get("home") or {}
    fora = times.get("away") or {}

    # A API-Football expõe national=true no objeto team quando disponível.
    if casa.get("national") is True or fora.get("national") is True:
        return True

    liga = jogo.get("league") or {}
    pais_liga = (liga.get("country") or "").strip().lower()
    nome_liga = (liga.get("name") or "").strip().lower()

    # Competições internacionais da API normalmente usam World como país.
    # Excluímos explicitamente competições de clubes que também vivem em World.
    clubes_world = (
        "champions league", "europa league", "conference league",
        "libertadores", "sudamericana", "club world cup",
        "intercontinental cup", "recopa", "youth league",
    )
    if pais_liga == "world" and not any(termo in nome_liga for termo in clubes_world):
        return True

    termos_selecoes = (
        "world cup", "copa america", "euro championship", "nations league",
        "qualification", "qualifiers", "friendly", "friendlies",
        "africa cup of nations", "asian cup", "gold cup", "nations cup",
        "olympics men", "olympics women", "u20", "u19", "u17",
    )
    return any(termo in nome_liga for termo in termos_selecoes)


def filtrar_jogos(jogos):
    filtrados = []
    for jogo in jogos:
        league_id = jogo.get("league", {}).get("id")
        if league_id in CAMPEONATOS:
            filtrados.append(jogo)
            continue
        if INCLUIR_JOGOS_SELECOES and _eh_selecao(jogo):
            filtrados.append(jogo)
    return filtrados


def exibir_jogos(jogos):
    print("\nJOGOS MONITORADOS")
    print("=" * 60)
    if not jogos:
        print("Nenhum jogo encontrado para hoje.")
        return
    for jogo in jogos:
        league = jogo.get("league") or {}
        league_id = league.get("id")
        campeonato = CAMPEONATOS.get(league_id, {})
        nome_campeonato = campeonato.get("nome") or league.get("name") or "Competição internacional"
        data_jogo = datetime.fromisoformat(
            jogo["fixture"]["date"].replace("Z", "+00:00")
        ).astimezone(TIMEZONE_BRASILIA)
        print(f"\nCompetição: {nome_campeonato}")
        print(f"Jogo: {jogo['teams']['home']['name']} x {jogo['teams']['away']['name']}")
        print(f"Horário: {data_jogo.strftime('%H:%M')}")
        print("-" * 60)


if __name__ == "__main__":
    filtrados = filtrar_jogos(buscar_jogos())
    print(f"Total monitorado: {len(filtrados)}")
    exibir_jogos(filtrados)
