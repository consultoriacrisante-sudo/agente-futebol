from estruturar_escalacoes import estruturar_escalacao
from extrair_lineups import extrair_lineup


# ============================================================
# FONTES PRIORITÁRIAS
# ============================================================

FONTES_PRIORITARIAS = {
    "whoscored.com": 1000,
    "sofascore.com": 800,
    "espn.com": 700,
    "goal.com": 600,
    "sportingnews.com": 500,
    "lance.com.br": 400,
    "365scores.com": 350,
    "fotmob.com": 300
}


# ============================================================
# PALAVRAS DE ESCALAÇÃO CONFIRMADA
# ============================================================

PALAVRAS_CONFIRMADAS = [
    "confirmed lineup",
    "confirmed lineups",
    "lineup confirmed",
    "lineups confirmed",
    "confirmed starting xi",
    "starting lineup confirmed",
    "starting lineups confirmed",
    "escalação confirmada",
    "escalações confirmadas",
    "escalação oficial",
    "escalações oficiais"
]


# ============================================================
# PALAVRAS DE PREVISÃO
# ============================================================

PALAVRAS_PREVISAO = [
    "prediction",
    "predictions",
    "predicted lineup",
    "expected lineup",
    "possible lineup",
    "probable lineup",
    "projected lineup",
    "palpite",
    "palpites",
    "betting",
    "odds",
    "picks",
    "provável escalação",
    "prováveis escalações",
    "escalação provável",
    "escalações prováveis"
]


# ============================================================
# CALCULAR PONTUAÇÃO
# ============================================================

def calcular_pontuacao(
    resultado,
    extracao,
    estrutura
):

    titulo = resultado.get(
        "title",
        ""
    )

    url = resultado.get(
        "url",
        ""
    )

    titulo_lower = titulo.lower()

    url_lower = url.lower()

    jogadores_casa = extracao.get(
        "jogadores_casa",
        []
    )

    jogadores_fora = extracao.get(
        "jogadores_fora",
        []
    )

    total_casa = len(
        jogadores_casa
    )

    total_fora = len(
        jogadores_fora
    )

    pontuacao = 0

    # ========================================================
    # FONTE ESPECÍFICA
    # ========================================================

    for dominio, pontos in FONTES_PRIORITARIAS.items():

        if dominio in url_lower:

            pontuacao += pontos

            break

    # ========================================================
    # ESCALAÇÃO CONFIRMADA
    # ========================================================

    if estrutura.get(
        "confirmada",
        False
    ):

        pontuacao += 500

    # ========================================================
    # TÍTULO CONFIRMADO
    # ========================================================

    for palavra in PALAVRAS_CONFIRMADAS:

        if palavra in titulo_lower:

            pontuacao += 300

            break

    # ========================================================
    # 11 JOGADORES EM CADA TIME
    # ========================================================

    if total_casa == 11:

        pontuacao += 150

    if total_fora == 11:

        pontuacao += 150

    # ========================================================
    # FORMAÇÃO
    # ========================================================

    if estrutura.get(
        "formacao"
    ):

        pontuacao += 50

    # ========================================================
    # PENALIZAR PREVISÃO
    # ========================================================

    for palavra in PALAVRAS_PREVISAO:

        if palavra in titulo_lower:

            pontuacao -= 200

            break

    return pontuacao


# ============================================================
# VALIDAR ESCALAÇÃO
# ============================================================

def escalação_valida(
    extracao
):

    jogadores_casa = extracao.get(
        "jogadores_casa",
        []
    )

    jogadores_fora = extracao.get(
        "jogadores_fora",
        []
    )

    # Precisamos dos dois times

    if not jogadores_casa:

        return False

    if not jogadores_fora:

        return False

    # Precisamos de 11 jogadores em cada time

    if len(jogadores_casa) == 11 and \
       len(jogadores_fora) == 11:

        return True

    return False


# ============================================================
# SELECIONAR MELHOR ESCALAÇÃO
# ============================================================

def selecionar_melhor_escalacao(
    resultados,
    time_casa,
    time_fora
):

    melhor_resultado = None

    melhor_extracao = None

    melhor_estrutura = None

    melhor_pontuacao = -1

    # ========================================================
    # ANALISAR TODAS AS FONTES
    # ========================================================

    for resultado in resultados:

        titulo = resultado.get(
            "title",
            ""
        )

        url = resultado.get(
            "url",
            ""
        )

        # ====================================================
        # EXTRAIR JOGADORES
        # ====================================================

        extracao = extrair_lineup(
            resultado,
            time_casa,
            time_fora
        )

        jogadores_casa = extracao.get(
            "jogadores_casa",
            []
        )

        jogadores_fora = extracao.get(
            "jogadores_fora",
            []
        )

        print()
        print("ANALISANDO FONTE")
        print("-" * 60)

        print(
            "Título:",
            titulo
        )

        print(
            "URL:",
            url
        )

        print(
            f"Jogadores {time_casa}:",
            len(jogadores_casa)
        )

        print(
            f"Jogadores {time_fora}:",
            len(jogadores_fora)
        )

        # ====================================================
        # ESTRUTURA
        # ====================================================

        estrutura = estruturar_escalacao(
            resultado
        )

        # ====================================================
        # VALIDAR
        # ====================================================

        if not escalação_valida(
            extracao
        ):

            print(
                "ESCALAÇÃO REJEITADA"
            )

            continue

        # ====================================================
        # CALCULAR PONTUAÇÃO
        # ====================================================

        pontuacao = calcular_pontuacao(
            resultado,
            extracao,
            estrutura
        )

        print(
            "ESCALAÇÃO ACEITA"
        )

        print(
            "Fonte:",
            url
        )

        print(
            "Confirmada:",
            estrutura.get(
                "confirmada",
                False
            )
        )

        print(
            "Pontuação:",
            pontuacao
        )

        # ====================================================
        # VERIFICAR MELHOR FONTE
        # ====================================================

        if pontuacao > melhor_pontuacao:

            melhor_pontuacao = pontuacao

            melhor_resultado = resultado

            melhor_extracao = extracao

            melhor_estrutura = estrutura

    # ========================================================
    # NENHUMA ESCALAÇÃO ENCONTRADA
    # ========================================================

    if melhor_resultado is None:

        return None

    # ========================================================
    # RETORNO PADRONIZADO
    # ========================================================

    jogadores_casa = melhor_extracao.get(
        "jogadores_casa",
        []
    )

    jogadores_fora = melhor_extracao.get(
        "jogadores_fora",
        []
    )

    return {

        "resultado": melhor_resultado,

        "extracao": {

            "jogadores":
                jogadores_casa +
                jogadores_fora,

            "jogadores_casa":
                jogadores_casa,

            "jogadores_fora":
                jogadores_fora,

            "total_jogadores":
                len(jogadores_casa) +
                len(jogadores_fora)
        },

        "estrutura":
            melhor_estrutura,

        "pontuacao":
            melhor_pontuacao
    }
