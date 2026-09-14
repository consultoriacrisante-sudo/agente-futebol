import os
import requests

from dotenv import load_dotenv


# ============================================================
# CONFIGURACAO
# ============================================================

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")

URL = "https://v3.football.api-sports.io/injuries"


# ============================================================
# BUSCAR DESFALQUES
# ============================================================

def buscar_desfalques(fixture_id):

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "fixture": fixture_id
    }

    response = requests.get(
        URL,
        headers=headers,
        params=params,
        timeout=30
    )

    if response.status_code != 200:

        print("Erro ao consultar desfalques.")
        print(f"Status HTTP: {response.status_code}")

        return []

    data = response.json()

    return data.get("response", [])


# ============================================================
# REMOVER DUPLICIDADES
# ============================================================

def remover_duplicados(desfalques):

    encontrados = set()
    resultado = []

    for item in desfalques:

        player_id = item["player"]["id"]
        fixture_id = item["fixture"]["id"]

        chave = (
            player_id,
            fixture_id
        )

        if chave in encontrados:
            continue

        encontrados.add(chave)

        resultado.append(item)

    return resultado


# ============================================================
# CLASSIFICAR DESFALQUE
# ============================================================

def classificar_desfalque(tipo, motivo):

    motivo_lower = motivo.lower()

    # Cartão amarelo ou vermelho
    if "yellow" in motivo_lower or "red" in motivo_lower:
        return "Suspenso"

    # Jogador confirmado como fora
    if tipo == "Missing Fixture":
        return "Fora"

    # Jogador ainda é dúvida
    if tipo == "Questionable":
        return "Dúvida"

    return "Indisponível"


# ============================================================
# FORMATAR DESFALQUES
# ============================================================

def formatar_desfalques(desfalques):

    desfalques = remover_duplicados(desfalques)

    resultado = []

    for item in desfalques:

        player = item["player"]
        team = item["team"]

        tipo = player["type"]
        motivo = player["reason"]

        status = classificar_desfalque(
            tipo,
            motivo
        )

        resultado.append({
            "jogador": player["name"],
            "time": team["name"],
            "status": status,
            "motivo": motivo,
            "motivo_pt": traduzir_motivo(motivo)
        })

    return resultado

# ============================================================
# TRADUZIR MOTIVO
# ============================================================

def traduzir_motivo(motivo):

    traducoes = {
        "Yellow Cards": "Cartões amarelos",
        "Red Card": "Cartão vermelho",
        "Calf Injury": "Lesão na panturrilha",
        "Knee Injury": "Lesão no joelho",
        "Hamstring Injury": "Lesão muscular",
        "Muscle Injury": "Lesão muscular",
        "Back Injury": "Lesão nas costas",
        "Ankle Injury": "Lesão no tornozelo",
        "Thigh Injury": "Lesão na coxa",
        "Shoulder Injury": "Lesão no ombro",
        "Knock": "Pancada",
        "Inactive": "Inativo",
        "Injury": "Lesão"
    }

    return traducoes.get(
        motivo,
        motivo
    )
