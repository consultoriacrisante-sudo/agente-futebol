from buscar_escalacoes import buscar_escalacoes
from estruturar_times import estruturar_times


# ============================================================
# TESTE DA ESTRUTURAÇÃO POR TIME
# ============================================================

print()
print("=" * 60)
print("TESTE DA ESTRUTURAÇÃO POR TIME")
print("=" * 60)

time_casa = "Marseille"
time_fora = "Strasbourg"
campeonato = "Ligue 1"
data = "21/08/2026"


print()
print(f"Buscando: {time_casa} x {time_fora}")


# ============================================================
# BUSCAR FONTES
# ============================================================

fontes = buscar_escalacoes(
    time_casa,
    time_fora,
    campeonato,
    data
)

print()
print(f"Total de fontes encontradas: {len(fontes)}")


# ============================================================
# LOCALIZAR ESCALAÇÃO CONFIRMADA
# ============================================================

fonte_confirmada = None

for fonte in fontes:

    titulo = fonte.get("title", "")
    conteudo = fonte.get("content", "")

    texto = (
        titulo + " " + conteudo
    ).lower()

    if (
        "confirmed lineup" in texto
        or "confirmed lineups" in texto
        or "starting lineup" in texto
    ):

        fonte_confirmada = fonte
        break


# ============================================================
# TESTAR
# ============================================================

if not fonte_confirmada:

    print()
    print("NENHUMA ESCALAÇÃO CONFIRMADA ENCONTRADA.")

else:

    dados = estruturar_times(
        fonte_confirmada,
        time_casa,
        time_fora
    )

    print()
    print("=" * 60)
    print("TIME DA CASA")
    print("=" * 60)

    print()
    print(dados["time_casa"])

    for numero, jogador in enumerate(
        dados["jogadores_casa"],
        start=1
    ):

        print(f"{numero}. {jogador}")

    print()
    print(
        f"Total: {dados['total_casa']}"
    )

    print()
    print("=" * 60)
    print("TIME FORA")
    print("=" * 60)

    print()
    print(dados["time_fora"])

    for numero, jogador in enumerate(
        dados["jogadores_fora"],
        start=1
    ):

        print(f"{numero}. {jogador}")

    print()
    print(
        f"Total: {dados['total_fora']}"
    )

print()
print("=" * 60)
