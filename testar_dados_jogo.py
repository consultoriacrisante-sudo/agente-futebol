from buscar_jogos import (
    buscar_jogos,
    filtrar_jogos
)

from buscar_escalacoes import (
    buscar_escalacoes
)

from selecionar_escalacao import (
    selecionar_melhor_escalacao
)

from dados_jogo import (
    montar_dados_jogo
)


# ============================================================
# TESTE DOS DADOS COMPLETOS DO JOGO
# ============================================================

print()
print("=" * 60)
print("TESTE DOS DADOS COMPLETOS DO JOGO")
print("=" * 60)


# ============================================================
# BUSCAR JOGOS
# ============================================================

print()
print("BUSCANDO JOGOS")
print("=" * 60)

jogos = buscar_jogos()

jogos_filtrados = filtrar_jogos(
    jogos
)

print()
print(
    f"Total de jogos monitorados: "
    f"{len(jogos_filtrados)}"
)


# ============================================================
# VERIFICAR JOGOS
# ============================================================

if not jogos_filtrados:

    print()
    print("Nenhum jogo encontrado.")

    exit()


# ============================================================
# SELECIONAR PRIMEIRO JOGO
# ============================================================

jogo = jogos_filtrados[0]

fixture_id = jogo["fixture"]["id"]

time_casa = jogo["teams"]["home"]["name"]

time_fora = jogo["teams"]["away"]["name"]

campeonato = jogo["league"]["name"]

data_jogo = jogo["fixture"]["date"]


# ============================================================
# EXIBIR JOGO
# ============================================================

print()
print("=" * 60)
print("JOGO SELECIONADO")
print("=" * 60)

print()
print(f"Fixture ID: {fixture_id}")
print(f"Jogo: {time_casa} x {time_fora}")
print(f"Campeonato: {campeonato}")
print(f"Data: {data_jogo}")


# ============================================================
# BUSCAR ESCALAÇÕES
# ============================================================

print()
print("=" * 60)
print("BUSCANDO ESCALAÇÕES")
print("=" * 60)

resultados = buscar_escalacoes(
    time_casa,
    time_fora,
    campeonato,
    data_jogo
)


print()
print(
    f"Total de fontes encontradas: "
    f"{len(resultados)}"
)


# ============================================================
# VERIFICAR RESULTADOS
# ============================================================

if not resultados:

    print()
    print(
        "Nenhuma fonte de escalação encontrada."
    )

    exit()


# ============================================================
# SELECIONAR MELHOR ESCALAÇÃO
# ============================================================

print()
print("=" * 60)
print("SELECIONANDO MELHOR ESCALAÇÃO")
print("=" * 60)


resultado_selecionado = selecionar_melhor_escalacao(
    resultados,
    time_casa,
    time_fora
)


# ============================================================
# VERIFICAR ESCALAÇÃO
# ============================================================

if not resultado_selecionado:

    print()
    print(
        "Nenhuma escalação válida encontrada."
    )

    print()
    print(
        "O jogo continuará sem escalação confirmada."
    )

else:

    print()
    print("=" * 60)
    print("MELHOR ESCALAÇÃO ENCONTRADA")
    print("=" * 60)

    resultado = resultado_selecionado.get(
        "resultado",
        {}
    )

    estrutura = resultado_selecionado.get(
        "estrutura",
        {}
    )

    extracao = resultado_selecionado.get(
        "extracao",
        {}
    )

    print()
    print(
        f"Título: "
        f"{resultado.get('title', '')}"
    )

    print()
    print(
        f"Fonte: "
        f"{resultado.get('url', '')}"
    )

    print()
    print(
        f"Pontuação: "
        f"{resultado_selecionado.get('pontuacao', 0)}"
    )

    print()
    print(
        f"Escalação confirmada: "
        f"{estrutura.get('confirmada', False)}"
    )

    print()
    print(
        f"Formação: "
        f"{estrutura.get('formacao')}"
    )

    print()
    print(
        f"Jogadores {time_casa}: "
        f"{len(extracao.get('jogadores_casa', []))}"
    )

    print()
    print(
        f"Jogadores {time_fora}: "
        f"{len(extracao.get('jogadores_fora', []))}"
    )


# ============================================================
# MONTAR DADOS COMPLETOS
# ============================================================

print()
print("=" * 60)
print("MONTANDO DADOS COMPLETOS DO JOGO")
print("=" * 60)


dados = montar_dados_jogo(
    jogo,
    resultado_selecionado
)


# ============================================================
# EXIBIR DADOS BÁSICOS
# ============================================================

print()
print("=" * 60)
print("DADOS DO JOGO")
print("=" * 60)

print()
print(
    f"Fixture ID: "
    f"{dados['fixture_id']}"
)

print(
    f"Campeonato: "
    f"{dados['campeonato']}"
)

print(
    f"Data: "
    f"{dados['data']}"
)

print(
    f"Jogo: "
    f"{dados['time_casa']} x "
    f"{dados['time_fora']}"
)


# ============================================================
# EXIBIR ESCALAÇÃO
# ============================================================

escalação = dados["escalação"]


print()
print("=" * 60)
print("ESCALAÇÃO")
print("=" * 60)


print()
print(
    f"Confirmada: "
    f"{escalação['escalação_confirmada']}"
)

print(
    f"Formação: "
    f"{escalação['formacao']}"
)


# ============================================================
# FONTE
# ============================================================

print()
print(
    f"Fonte: "
    f"{escalação['fonte']}"
)

print(
    f"Título: "
    f"{escalação['titulo_fonte']}"
)

print(
    f"Pontuação: "
    f"{escalação.get('pontuacao', 0)}"
)


# ============================================================
# TIME DA CASA
# ============================================================

print()
print(
    f"{dados['time_casa'].upper()}"
)

print("-" * 60)


for i, jogador in enumerate(
    escalação["jogadores_casa"],
    start=1
):

    print(
        f"{i}. {jogador}"
    )


print()
print(
    f"Total: "
    f"{escalação['total_casa']}"
)


# ============================================================
# TIME FORA
# ============================================================

print()
print(
    f"{dados['time_fora'].upper()}"
)

print("-" * 60)


for i, jogador in enumerate(
    escalação["jogadores_fora"],
    start=1
):

    print(
        f"{i}. {jogador}"
    )


print()
print(
    f"Total: "
    f"{escalação['total_fora']}"
)


# ============================================================
# EXIBIR DESFALQUES
# ============================================================

desfalques = dados["desfalques"]


print()
print("=" * 60)
print("DESFALQUES")
print("=" * 60)


print()
print(
    f"Total de desfalques: "
    f"{desfalques['total']}"
)


if desfalques["total"] == 0:

    print()
    print(
        "Nenhum desfalque encontrado."
    )

else:

    print()

    for i, desfalque in enumerate(
        desfalques["desfalques"],
        start=1
    ):

        print(
            f"{i}. "
            f"{desfalque['jogador']}"
        )

        print(
            f"   Time: "
            f"{desfalque['time']}"
        )

        print(
            f"   Status: "
            f"{desfalque['status']}"
        )

        print(
            f"   Motivo: "
            f"{desfalque['motivo_pt']}"
        )

        print()


# ============================================================
# STATUS FINAL
# ============================================================

print()
print("=" * 60)
print("STATUS")
print("=" * 60)

print()

if resultado_selecionado:

    print(
        "OK - dados completos do jogo estruturados"
    )

else:

    print(
        "OK - jogo estruturado, "
        "mas sem escalação válida disponível"
    )

print()