from config import CAMPEONATOS


print("CAMPEONATOS CONFIGURADOS")
print("=" * 60)

for league_id, campeonato in CAMPEONATOS.items():

    print(
        f'ID: {league_id} | '
        f'{campeonato["nome"]} | '
        f'{campeonato["pais"]} | '
        f'{campeonato["tipo"]}'
    )

print("=" * 60)
print(f"Total de competicoes: {len(CAMPEONATOS)}")