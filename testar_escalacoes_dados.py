from buscar_jogos import buscar_jogos, filtrar_jogos
from formatar_jogos import formatar_jogo
from buscar_escalacoes import buscar_escalacoes


jogos = filtrar_jogos(buscar_jogos())


print("=" * 60)
print("TESTE DOS DADOS DE ESCALAÇÃO")
print("=" * 60)


for jogo in jogos:

    resultado = formatar_jogo(jogo)

    print()
    print(
        f'{resultado["time_casa"]} x '
        f'{resultado["time_fora"]}'
    )

    fontes = buscar_escalacoes(
        resultado["time_casa"],
        resultado["time_fora"],
        resultado["campeonato"],
        resultado["data"]
    )

    print(f"Total de fontes: {len(fontes)}")

    for fonte in fontes:

        print()
        print("CHAVES DISPONÍVEIS:")
        print(fonte.keys())

        print()
        print("TÍTULO:")
        print(fonte.get("title"))

        print()
        print("URL:")
        print(fonte.get("url"))

        print()
        print("CONTEÚDO:")
        print(fonte.get("content"))

        print("-" * 60)
