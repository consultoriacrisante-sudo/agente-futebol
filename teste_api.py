import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# ============================================================
# CONFIGURAÇÃO
# ============================================================

load_dotenv()

api_key = os.getenv("API_FOOTBALL_KEY")

if not api_key:
    print("API Key não encontrada.")
    exit()

# ============================================================
# CONSULTA À API
# ============================================================

url = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": api_key
}

params = {
    "date": "2026-08-20"
}

response = requests.get(
    url,
    headers=headers,
    params=params
)

# ============================================================
# TRATAMENTO DA RESPOSTA
# ============================================================

if response.status_code != 200:
    print("Erro ao consultar a API.")
    print("Status:", response.status_code)
    print(response.text)
    exit()

data = response.json()

jogos = data["response"]

print()
print(" =========================================")
print("        JOGOS DE FUTEBOL - HOJE")
print("==========================================")
print()

print(f"Total de jogos encontrados: {len(jogos)}")
print()

# ============================================================
# EXIBIR JOGOS
# ============================================================

for jogo in jogos:

    campeonato = jogo["league"]["name"]

    time_casa = jogo["teams"]["home"]["name"]

    time_fora = jogo["teams"]["away"]["name"]

    horario = jogo["fixture"]["date"]

    # Converte a data da API para um formato mais amigável
    horario_formatado = datetime.fromisoformat(
        horario.replace("Z", "+00:00")
    )

    horario_formatado = horario_formatado.strftime("%d/%m/%Y %H:%M")

    print(f" {campeonato}")
    print(f" {time_casa} x {time_fora}")
    print(f" {horario_formatado}")
    print("-" * 50)