from buscar_jogos import buscar_jogos, filtrar_jogos
from formatar_jogos import formatar_jogo
from buscar_escalacoes import buscar_escalacoes


print()
print("BUSCANDO JOGOS")
print("=" * 60)
print("Data: 2026-08-21")
print()


jogos = filtrar_jogos(
    buscar_jogos()
)


print()
print("TESTE DA PESQUISA DE ESCALAÇÕES")
print("=" * 60)


for jogo in jogos:

    resultado = formatar_jogo(jogo)

    print()
    print(
        f'Consulta: '
        f'{resultado["time_casa"]} x '
        f'{resultado["time_fora"]} '
        f'{resultado["campeonato"]} '
        f'{resultado["data"]} '
        f'prováveis escalações'
    )

    fontes = buscar_escalacoes(
        resultado["time_casa"],
        resultado["time_fora"],
        resultado["campeonato"],
        resultado["data"]
    )

    print()
    print("FONTES ENCONTRADAS")
    print("-" * 60)

    for fonte in fontes:

        print()
        print(f'Título: {fonte.get("title")}')
        print(f'Score: {fonte.get("score")}')
        print(f'URL: {fonte.get("url")}')
        print(
            f'Descrição: '
            f'{fonte.get("content", "")[:500]}'
        )

    print()
    print("=" * 60)

