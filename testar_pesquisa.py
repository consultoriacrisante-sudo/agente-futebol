from buscar_jogos import buscar_jogos, filtrar_jogos
from formatar_jogos import formatar_jogo
from pesquisar_transmissoes import (
    pesquisar_transmissao,
    exibir_resultado
)


jogos = buscar_jogos()

jogos_filtrados = filtrar_jogos(jogos)


print()
print("TESTE DA PESQUISA DE TRANSMISSAO")
print("=" * 60)


contador = 0

for jogo in jogos_filtrados:

    resultado = formatar_jogo(jogo)

    pesquisa = pesquisar_transmissao(
        resultado
    )

    exibir_resultado(pesquisa)

    contador += 1

    if contador >= 3:
        break
