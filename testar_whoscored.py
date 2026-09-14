from buscar_escalacoes import buscar_escalacoes


time_casa = "Marseille"
time_fora = "Strasbourg"
campeonato = "Ligue 1"
data = "2026-08-21"


resultados = buscar_escalacoes(
    time_casa,
    time_fora,
    campeonato,
    data
)


for resultado in resultados:

    titulo = resultado.get("title", "")
    url = resultado.get("url", "")

    if "whoscored.com" in url.lower():

        print("=" * 70)
        print("WHO SCORED ENCONTRADO")
        print("=" * 70)

        print()
        print("TÍTULO:")
        print(titulo)

        print()
        print("URL:")
        print(url)

        print()
        print("CONTENT:")
        print("-" * 70)

        print(
            resultado.get(
                "content",
                ""
            )
        )

        print()
        print("=" * 70)

        break
