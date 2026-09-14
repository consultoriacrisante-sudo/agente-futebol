from buscar_escalacoes import buscar_escalacoes
from extrair_lineups import extrair_lineup


# ============================================================
# CONFIGURAÇÃO DO TESTE
# ============================================================

time_casa = "Marseille"
time_fora = "Strasbourg"

campeonato = "Ligue 1"

data = "2026-08-21"


# ============================================================
# BUSCAR FONTES
# ============================================================

print()
print("=" * 60)
print("TESTE DA EXTRAÇÃO DE LINEUPS")
print("=" * 60)

print()
print(f"Buscando: {time_casa} x {time_fora}")

fontes = buscar_escalacoes(
    time_casa,
    time_fora,
    campeonato,
    data
)

print()
print(f"Total de fontes encontradas: {len(fontes)}")


# ============================================================
# TESTAR TODAS AS FONTES
# ============================================================

for indice, fonte in enumerate(fontes, start=1):

    resultado = extrair_lineup(
        fonte,
        time_casa,
        time_fora
    )

    print()
    print("=" * 60)
    print(f"FONTE {indice}")
    print("=" * 60)

    print()
    print("Título:")
    print(fonte.get("title", ""))

    print()
    print("URL:")
    print(fonte.get("url", ""))

    print()
    print("MARSEILLE")
    print("-" * 60)

    for numero, jogador in enumerate(
        resultado["jogadores_casa"],
        start=1
    ):

        print(f"{numero}. {jogador}")

    print()
    print(
        f"Total Marseille: "
        f"{resultado['total_casa']}"
    )

    print()
    print("STRASBOURG")
    print("-" * 60)

    for numero, jogador in enumerate(
        resultado["jogadores_fora"],
        start=1
    ):

        print(f"{numero}. {jogador}")

    print()
    print(
        f"Total Strasbourg: "
        f"{resultado['total_fora']}"
    )
