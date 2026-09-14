from buscar_jogos import buscar_jogos, filtrar_jogos
from formatar_jogos import formatar_jogo


jogos = buscar_jogos()

jogos_filtrados = filtrar_jogos(jogos)


print("=" * 60)
print("TESTE DO JOGO FORMATADO")
print("=" * 60)


for jogo in jogos_filtrados:

    resultado = formatar_jogo(jogo)

    if resultado["status"] not in ["NS", "1H", "HT", "2H"]:
        continue

    print()
    print(f'Competição: {resultado["campeonato"]}')
    print(
        f'Jogo: {resultado["time_casa"]} '
        f'x {resultado["time_fora"]}'
    )
    print(f'Data: {resultado["data"]}')
    print(f'Horário: {resultado["horario"]}')
    print(f'Rodada: {resultado["rodada"]}')
    print(f'Temporada: {resultado["temporada"]}')
    print(f'Estádio: {resultado["estadio"]}')
    print(f'Cidade: {resultado["cidade"]}')
    print(f'Árbitro: {resultado["arbitro"]}')
    print(f'Status: {resultado["status"]}')
    print(f'Status detalhado: {resultado["status_detalhado"]}')
    print(f'Fixture ID: {resultado["fixture_id"]}')

    print("-" * 60)
