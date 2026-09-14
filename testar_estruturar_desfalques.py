from desfalques import estruturar_desfalques


print()
print("=" * 60)
print("TESTE DA ESTRUTURAÇÃO DE DESFALQUES")
print("=" * 60)


# ============================================================
# FIXTURE DE TESTE
# ============================================================

fixture_id = 1550089


print()
print("Fixture ID:")
print(fixture_id)


# ============================================================
# BUSCAR DESFALQUES
# ============================================================

resultado = estruturar_desfalques(fixture_id)


# ============================================================
# RESULTADO
# ============================================================

print()
print("=" * 60)
print("RESULTADO")
print("=" * 60)


print()
print("Total de desfalques:")
print(resultado["total"])


print()
print("DESFALQUES")
print("-" * 60)


if resultado["total"] == 0:

    print("Nenhum desfalque encontrado.")

else:

    for numero, item in enumerate(
        resultado["desfalques"],
        start=1
    ):

        print()
        print(f"{numero}. {item['jogador']}")
        print(f"   Time: {item['time']}")
        print(f"   Status: {item['status']}")
        print(f"   Motivo: {item['motivo_pt']}")


print()
print("=" * 60)

