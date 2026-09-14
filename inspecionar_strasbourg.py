from buscar_escalacoes import buscar_escalacoes


print()
print("=" * 60)
print("INSPEÇÃO DO TEXTO DO STRASBOURG")
print("=" * 60)


time_casa = "Marseille"
time_fora = "Strasbourg"
campeonato = "Ligue 1"
data = "21/08/2026"


fontes = buscar_escalacoes(
    time_casa,
    time_fora,
    campeonato,
    data
)


print()
print(f"Total de fontes encontradas: {len(fontes)}")


for numero, fonte in enumerate(fontes, start=1):

    titulo = fonte.get("title", "")
    conteudo = fonte.get("content", "")

    if "whoscored" in fonte.get("url", "").lower():

        print()
        print("=" * 60)
        print(f"FONTE WHOSCORED - {numero}")
        print("=" * 60)

        print()
        print("TÍTULO:")
        print(titulo)

        print()
        print("URL:")
        print(fonte.get("url", ""))

        print()
        print("TEXTO COMPLETO:")
        print("-" * 60)
        print(conteudo)
        print("-" * 60)

