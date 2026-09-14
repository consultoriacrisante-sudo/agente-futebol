from buscar_escalacoes import buscar_escalacoes
from selecionar_escalacao import selecionar_melhor_escalacao


# ============================================================
# TESTE
# ============================================================

time_casa = "Marseille"
time_fora = "Strasbourg"

campeonato = "Ligue 1"

data = "2026-08-21"


print()
print("=" * 60)
print("TESTE DA SELEÇÃO DA MELHOR FONTE")
print("=" * 60)

print()

print(
    f"Buscando: {time_casa} x {time_fora}"
)

resultados = buscar_escalacoes(
    time_casa,
    time_fora,
    campeonato,
    data
)

print()

print(
    f"Total de fontes encontradas: {len(resultados)}"
)

print()

resultado = selecionar_melhor_escalacao(
    resultados,
    time_casa,
    time_fora
)

print("=" * 60)
print("MELHOR FONTE")
print("=" * 60)

if not resultado:

    print()
    print("Nenhuma fonte adequada encontrada.")

else:

    fonte = resultado["resultado"]

    estrutura = resultado["estrutura"]

    extracao = resultado["extracao"]

    print()

    print("Título:")
    print(
        fonte.get(
            "title",
            ""
        )
    )

    print()

    print("URL:")
    print(
        fonte.get(
            "url",
            ""
        )
    )

    print()

    print("Pontuação:")
    print(
        resultado["pontuacao"]
    )

    print()

    print("Escalação confirmada:")
    print(
        estrutura["confirmada"]
    )

    print()

    print("Formação:")
    print(
        estrutura["formacao"]
    )

    print()

    print("Jogadores encontrados:")
    print("-" * 60)

    for numero, jogador in enumerate(
        extracao["jogadores"],
        1
    ):

        print(
            f"{numero}. {jogador}"
        )

    print()

    print(
        f"Total de jogadores: "
        f"{extracao['total_jogadores']}"
    )

print()
print("=" * 60)
