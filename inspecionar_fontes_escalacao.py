from buscar_escalacoes import buscar_escalacoes


# ============================================================
# INSPECIONAR FONTES DE ESCALAÇÃO
# ============================================================

time_casa = "Marseille"
time_fora = "Strasbourg"
campeonato = "Ligue 1"
data = "2026-08-21"


print()
print("=" * 60)
print("INSPEÇÃO DAS FONTES DE ESCALAÇÃO")
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


# ============================================================
# EXIBIR TODAS AS FONTES
# ============================================================

for numero, resultado in enumerate(
    resultados,
    1
):

    titulo = resultado.get(
        "title",
        ""
    )

    url = resultado.get(
        "url",
        ""
    )

    conteudo = resultado.get(
        "content",
        ""
    )

    print("=" * 60)

    print(
        f"FONTE {numero}"
    )

    print("=" * 60)

    print()

    print("TÍTULO:")
    print(titulo)

    print()

    print("URL:")
    print(url)

    print()

    print("CONTEÚDO:")
    print("-" * 60)

    print(conteudo)

    print()

    print("=" * 60)

    print()

