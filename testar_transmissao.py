from buscar_jogos import buscar_jogos, filtrar_jogos
from formatar_jogos import formatar_jogo
from transmissoes import exibir_consulta


jogos = buscar_jogos()

jogos_filtrados = filtrar_jogos(jogos)


print()
print("TESTE DO MÓDULO DE TRANSMISSÃO")
print("=" * 60)


for jogo in jogos_filtrados:

    resultado = formatar_jogo(jogo)

    if resultado["status"] != "NS":
        continue

    exibir_consulta(resultado)