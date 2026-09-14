from buscar_jogos import buscar_jogos, filtrar_jogos
from buscar_escalacoes import buscar_escalacoes


print()
print("=" * 70)
print("DIAGNÓSTICO 365SCORES")
print("=" * 70)


# ============================================================
# BUSCAR JOGOS
# ============================================================

jogos = filtrar_jogos(
    buscar_jogos()
)


if not jogos:

    print("Nenhum jogo encontrado.")
    exit()


# ============================================================
# PRIMEIRO JOGO
# ============================================================

jogo = jogos[0]

time_casa = jogo["teams"]["home"]["name"]
time_fora = jogo["teams"]["away"]["name"]
campeonato = jogo["league"]["name"]
data_jogo = jogo["fixture"]["date"]


print()
print("JOGO")
print("-" * 70)
print("Casa:", time_casa)
print("Fora:", time_fora)
print("Campeonato:", campeonato)
print("Data:", data_jogo)


# ============================================================
# BUSCAR FONTES
# ============================================================

resultados = buscar_escalacoes(
    time_casa,
    time_fora,
    campeonato,
    data_jogo
)


print()
print("TOTAL DE FONTES:", len(resultados))


# ============================================================
# PROCURAR 365SCORES
# ============================================================

encontrou = False


for resultado in resultados:

    url = resultado.get(
        "url",
        ""
    )

    if "365scores.com" not in url.lower():

        continue

    encontrou = True

    titulo = resultado.get(
        "title",
        ""
    )

    content = resultado.get(
        "content",
        ""
    )

    print()
    print("=" * 70)
    print("FONTE 365SCORES")
    print("=" * 70)

    print()
    print("TÍTULO:")
    print(titulo)

    print()
    print("URL:")
    print(url)

    print()
    print("TAMANHO DO CONTENT:")
    print(len(content))

    print()
    print("CONTENT COMPLETO:")
    print("-" * 70)

    print(content)

    print()
    print("-" * 70)


if not encontrou:

    print()
    print("NENHUMA FONTE 365SCORES ENCONTRADA.")
