# ============================================================
# MONTAR ESCALAÇÃO FINAL
# ============================================================

def montar_escalacao_final(
    resultado_selecionado,
    time_casa,
    time_fora
):

    # ========================================================
    # VALIDAR RESULTADO
    # ========================================================

    if not resultado_selecionado:

        return {
            "time_casa": time_casa,
            "time_fora": time_fora,
            "escalação_confirmada": False,
            "formacao": None,
            "jogadores_casa": [],
            "jogadores_fora": [],
            "total_casa": 0,
            "total_fora": 0,
            "fonte": None,
            "titulo_fonte": None
        }

    # ========================================================
    # PEGAR ESTRUTURA E EXTRAÇÃO JÁ SELECIONADAS
    # ========================================================

    estrutura = resultado_selecionado.get(
        "estrutura",
        {}
    )

    extracao = resultado_selecionado.get(
        "extracao",
        {}
    )

    resultado = resultado_selecionado.get(
        "resultado",
        {}
    )

    # ========================================================
    # JOGADORES
    # ========================================================

    jogadores_casa = extracao.get(
        "jogadores_casa",
        []
    )

    jogadores_fora = extracao.get(
        "jogadores_fora",
        []
    )

    # ========================================================
    # RESULTADO FINAL
    # ========================================================

    return {

        "time_casa": time_casa,

        "time_fora": time_fora,

        "escalação_confirmada": estrutura.get(
            "confirmada",
            False
        ),

        "formacao": estrutura.get(
            "formacao"
        ),

        "jogadores_casa": jogadores_casa,

        "jogadores_fora": jogadores_fora,

        "total_casa": len(
            jogadores_casa
        ),

        "total_fora": len(
            jogadores_fora
        ),

        "fonte": resultado.get(
            "url",
            ""
        ),

        "titulo_fonte": resultado.get(
            "title",
            ""
        ),

        "pontuacao": resultado_selecionado.get(
            "pontuacao",
            0
        )
    }