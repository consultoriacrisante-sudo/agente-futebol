from buscar_lineups import buscar_lineups


# ============================================================
# TESTE
# ============================================================

fixture_id = 1622626


print()
print("=" * 60)
print("TESTE DA API DE ESCALAÇÕES")
print("=" * 60)

print()
print(f"Fixture ID: {fixture_id}")

print()
print("CONSULTANDO API-FOOTBALL")
print("-" * 60)


resultado = buscar_lineups(fixture_id)


print()
print(f"Total de times retornados: {len(resultado)}")


print()
print("=" * 60)
print("RESULTADO")
print("=" * 60)


for lineup in resultado:

    team = lineup.get("team", {})

    print()
    print(f"TIME: {team.get('name')}")

    print(
        f"Formação: "
        f"{lineup.get('formation')}"
    )

    print()
    print("TITULARES")
    print("-" * 60)

    start_xi = lineup.get("startXI", [])

    for jogador in start_xi:

        player = jogador.get("player", {})

        print(
            f'{player.get("number")}. '
            f'{player.get("name")}'
        )

    print()
    print("RESERVAS")
    print("-" * 60)

    substitutes = lineup.get("substitutes", [])

    for jogador in substitutes:

        player = jogador.get("player", {})

        print(
            f'{player.get("number")}. '
            f'{player.get("name")}'
        )

    print()
    print(
        f'Técnico: '
        f'{lineup.get("coach", {}).get("name")}'
    )
