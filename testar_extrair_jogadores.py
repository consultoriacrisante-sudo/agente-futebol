from buscar_escalacoes import buscar_escalacoes
from extrair_jogadores import extrair_jogadores


# ============================================================
# TESTE DA EXTRAÇÃO DE JOGADORES
# ============================================================

print()
print("=" * 60)
print("TESTE DA EXTRAÇÃO DE JOGADORES")
print("=" * 60)

time_casa = "Marseille"
time_fora = "Strasbourg"
campeonato = "Ligue 1"
data = "21/08/2026"


print()
print(f"Buscando: {time_casa} x {time_fora}")

fontes = buscar_escalacoes(
    time_casa,
    time_fora,
    campeonato,
    data
)

print()
print(f"Total de fontes encontradas: {len(fontes)}")


# ============================================================
# PROCURAR FONTE DE ESCALAÇÃO CONFIRMADA
# ============================================================

fonte_confirmada = None

for fonte in fontes:

    titulo = fonte.get("title", "")
    conteudo = fonte.get("content", "")

    texto = (titulo + " " + conteudo).lower()

    if (
        "confirmed lineup" in texto
        or "confirmed lineups" in texto
        or "starting lineup" in texto
    ):

        fonte_confirmada = fonte
        break


# ============================================================
# VALIDAR RESULTADO
# ============================================================

if not fonte_confirmada:

    print()
    print("NENHUMA ESCALAÇÃO CONFIRMADA ENCONTRADA.")

else:

    print()
    print("=" * 60)
    print("FONTE CONFIRMADA ENCONTRADA")
    print("=" * 60)

    print()
    print("Título:")
    print(fonte_confirmada.get("title", ""))

    print()
    print("URL:")
    print(fonte_confirmada.get("url", ""))

    dados = extrair_jogadores(fonte_confirmada)

    print()
    print("JOGADORES ENCONTRADOS")
    print("-" * 60)

    for numero, jogador in enumerate(
        dados["jogadores"],
        start=1
    ):

        print(f"{numero}. {jogador}")

    print()
    print(f"TOTAL DE JOGADORES: {dados['total_jogadores']}")

print()
print("=" * 60)
