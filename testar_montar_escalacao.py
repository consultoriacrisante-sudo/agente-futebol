from buscar_escalacoes import buscar_escalacoes
from selecionar_escalacao import selecionar_melhor_escalacao
from montar_escalacao_final import montar_escalacao_final


# ============================================================
# TESTE DA ESCALAÇÃO FINAL
# ============================================================

time_casa = "Marseille"
time_fora = "Strasbourg"
campeonato = "Ligue 1"
data = "2026-08-21"


print("=" * 60)
print("TESTE DA ESCALAÇÃO FINAL")
print("=" * 60)

print()
print(f"Buscando: {time_casa} x {time_fora}")
print()


# ============================================================
# BUSCAR FONTES
# ============================================================

resultados = buscar_escalacoes(
    time_casa,
    time_fora,
    campeonato,
    data
)

print(
    f"Total de fontes encontradas: {len(resultados)}"
)


# ============================================================
# SELECIONAR MELHOR ESCALAÇÃO
# ============================================================

resultado_selecionado = selecionar_melhor_escalacao(
    resultados,
    time_casa,
    time_fora
)


# ============================================================
# VALIDAR SE ENCONTROU
# ============================================================

if not resultado_selecionado:

    print()
    print("=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    print()
    print("Nenhuma escalação válida encontrada.")

    raise SystemExit


# ============================================================
# MONTAR ESCALAÇÃO FINAL
# ============================================================

escalação = montar_escalacao_final(
    resultado_selecionado,
    time_casa,
    time_fora
)


# ============================================================
# RESULTADO
# ============================================================

print()
print("=" * 60)
print("RESULTADO FINAL")
print("=" * 60)

print()

print(
    f"Fonte: {escalação['titulo_fonte']}"
)

print(
    f"URL: {escalação['fonte']}"
)

print(
    f"Escalação confirmada: "
    f"{escalação['escalação_confirmada']}"
)

print(
    f"Formação: "
    f"{escalação['formacao']}"
)

print()

print("MARSEILLE")
print("-" * 60)

for i, jogador in enumerate(
    escalação["jogadores_casa"],
    start=1
):

    print(f"{i}. {jogador}")

print(
    f"Total Marseille: "
    f"{escalação['total_casa']}"
)

print()

print("STRASBOURG")
print("-" * 60)

for i, jogador in enumerate(
    escalação["jogadores_fora"],
    start=1
):

    print(f"{i}. {jogador}")

print(
    f"Total Strasbourg: "
    f"{escalação['total_fora']}"
)

print()

print("=" * 60)
print("TESTE CONCLUÍDO")
print("=" * 60)
