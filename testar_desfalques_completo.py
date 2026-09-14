from buscar_jogos import buscar_jogos, filtrar_jogos
from formatar_jogos import formatar_jogo
from buscar_desfalques import (
    buscar_desfalques,
    formatar_desfalques
)


jogos = buscar_jogos()

jogos_filtrados = filtrar_jogos(jogos)


print()
print("=" * 60)
print("TESTE DE DESFALQUES POR JOGO")
print("=" * 60)


contador = 0


for jogo in jogos_filtrados:

    resultado = formatar_jogo(jogo)

    if resultado["status"] not in ["NS", "1H", "HT", "2H"]:
        continue

    print()
    print("=" * 60)
    print(
        f'{resultado["time_casa"]} '
        f'x {resultado["time_fora"]}'
    )
    print("=" * 60)

    dados = buscar_desfalques(
        resultado["fixture_id"]
    )

    desfalques = formatar_desfalques(
        dados
    )

    print()
    print(f"Total retornado pela API: {len(dados)}")
    print(f"Total após tratamento: {len(desfalques)}")

    print()
    print("DESFALQUES")
    print("-" * 60)

    if not desfalques:

        print("Nenhum desfalque encontrado.")

    else:

        for item in desfalques:

            print(
                f'{item["time"]} | '
                f'{item["jogador"]} | '
                f'{item["status"]} | '
                f'{item["motivo_pt"]}'
            )

    contador += 1

    if contador >= 3:
        break
