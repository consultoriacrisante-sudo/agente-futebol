import re


# ============================================================
# ESTRUTURAR ESCALAÇÕES POR TIME
# ============================================================

def extrair_linha_starting_lineup(texto, time):

    texto_minusculo = texto.lower()
    time_minusculo = time.lower()

    marcador = time_minusculo + " starting lineup:"

    posicao = texto_minusculo.find(marcador)

    if posicao == -1:
        return None

    inicio = posicao + len(marcador)

    restante = texto[inicio:]

    # A escalação termina no primeiro ponto.
    fim = restante.find(".")

    if fim == -1:
        linha = restante
    else:
        linha = restante[:fim]

    return linha.strip()


def limpar_jogadores(linha):

    if not linha:
        return []

    jogadores = []

    partes = linha.split(",")

    for parte in partes:

        jogador = parte.strip()

        jogador = jogador.rstrip(".,[];:")

        jogador = jogador.strip()

        if jogador:
            jogadores.append(jogador)

    return jogadores


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def estruturar_times(resultado, time_casa, time_fora):

    titulo = resultado.get("title", "")
    conteudo = resultado.get("content", "")

    # ========================================================
    # TIME DA CASA
    # ========================================================

    linha_casa = extrair_linha_starting_lineup(
        conteudo,
        time_casa
    )

    jogadores_casa = limpar_jogadores(
        linha_casa
    )

    # ========================================================
    # TIME FORA
    # ========================================================

    linha_fora = extrair_linha_starting_lineup(
        conteudo,
        time_fora
    )

    jogadores_fora = limpar_jogadores(
        linha_fora
    )

    # ========================================================
    # RETORNO
    # ========================================================

    return {
        "titulo": titulo,
        "time_casa": time_casa,
        "time_fora": time_fora,
        "jogadores_casa": jogadores_casa,
        "jogadores_fora": jogadores_fora,
        "total_casa": len(jogadores_casa),
        "total_fora": len(jogadores_fora)
    }
