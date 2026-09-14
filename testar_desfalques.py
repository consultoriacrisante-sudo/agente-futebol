from buscar_desfalques import (
    buscar_desfalques,
    formatar_desfalques
)


fixture_id = 1552733


print("=" * 60)
print("TESTE DE DESFALQUES")
print("=" * 60)


desfalques = buscar_desfalques(fixture_id)

resultado = formatar_desfalques(desfalques)


print()
print(f"Total retornado pela API: {len(desfalques)}")
print(
    f"Total após remover duplicados: "
    f"{len(resultado)}"
)

print()
print("DESFALQUES")
print("-" * 60)


for item in resultado:

    print(
    f'{item["time"]} | '
    f'{item["jogador"]} | '
    f'{item["status"]} | '
    f'{item["motivo_pt"]}'
)
