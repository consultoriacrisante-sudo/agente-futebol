from buscar_jogos import buscar_jogos, filtrar_jogos
from formatar_jogos import formatar_jogo


jogos = buscar_jogos()

jogos_filtrados = filtrar_jogos(jogos)


print()
print("JOGOS FORMATADOS")
print("=" * 60)


for jogo in jogos_filtrados:

    resultado = formatar_jogo(jogo)

    print(resultado)