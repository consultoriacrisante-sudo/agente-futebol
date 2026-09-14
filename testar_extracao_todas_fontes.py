from buscar_escalacoes import buscar_escalacoes
from extrair_jogadores import extrair_jogadores


# ============================================================
# TESTAR TODAS AS FONTES
# ============================================================

time_casa = "Marseille"
time_fora = "Strasbourg"
campeonato = "Ligue 1"
data = "2026-08-21"


print()
print("=" * 60)
print("TESTE DE EXTRAÇÃO EM TODAS AS FONTES")
print("=" * 60)

resultados = buscar_escalacoes(
    time_casa,
    time_fora,
    campeonato,
    data
)

print()
print(f"Total de fontes encontradas: {len(resultados)}")


for indice, fonte in enumerate(resultados, start=1):

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

    resultado = extrair_jogadores(fonte)

    print()
    print("JOGADORES EXTRAÍDOS")
    print("-" * 60)

    jogadores = resultado["jogadores"]

    if not jogadores:

        print("Nenhum jogador encontrado.")

    else:

        for numero, jogador in enumerate(
            jogadores,
            start=1
        ):

            print(
                f"{numero}. {jogador}"
            )

    print()
    print(
        f"TOTAL: {resultado['total_jogadores']}"
    )

print()
print("=" * 60)
print("FIM DO TESTE")
print("=" * 60)

