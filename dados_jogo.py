from montar_escalacao_final import montar_escalacao_final
from desfalques import estruturar_desfalques
from pesquisar_transmissoes import pesquisar_transmissao

from datetime import datetime


# ============================================================
# SEPARAR DATA E HORÁRIO DE UMA STRING ISO 8601
# ============================================================

def separar_data_horario(data_iso):
    """
    Recebe a data no formato ISO 8601 (ex: '2026-08-27T20:00:00+00:00')
    e devolve (data 'DD/MM/AAAA', horario 'HH:MM').

    Se o parsing falhar por qualquer motivo, devolve a string original
    nos dois campos, para não quebrar o pipeline por causa da busca
    de transmissão.
    """

    try:

        momento = datetime.fromisoformat(data_iso)

        data_formatada = momento.strftime("%d/%m/%Y")

        horario_formatado = momento.strftime("%H:%M")

        return data_formatada, horario_formatado

    except Exception:

        return data_iso, data_iso


# ============================================================
# MONTAR DADOS COMPLETOS DO JOGO
# ============================================================

def montar_dados_jogo(
    jogo,
    resultado_selecionado
):

    # ========================================================
    # DADOS BÁSICOS DO JOGO
    # ========================================================

    fixture_id = jogo["fixture"]["id"]

    time_casa = jogo["teams"]["home"]["name"]

    time_fora = jogo["teams"]["away"]["name"]

    campeonato = jogo["league"]["name"]

    data_jogo = jogo["fixture"]["date"]

    data_formatada, horario_formatado = separar_data_horario(
        data_jogo
    )

    # ========================================================
    # MONTAR ESCALAÇÃO FINAL
    # ========================================================

    escalação = montar_escalacao_final(
        resultado_selecionado,
        time_casa,
        time_fora
    )

    # ========================================================
    # BUSCAR DESFALQUES
    # ========================================================

    desfalques = estruturar_desfalques(
        fixture_id
    )

    # ========================================================
    # BUSCAR TRANSMISSÃO
    # ========================================================

    jogo_para_transmissao = {

        "time_casa": time_casa,

        "time_fora": time_fora,

        "campeonato": campeonato,

        "data": data_formatada,

        "horario": horario_formatado
    }

    transmissao = pesquisar_transmissao(
        jogo_para_transmissao
    )

    # ========================================================
    # RETORNAR DADOS COMPLETOS
    # ========================================================

    return {

        "fixture_id": fixture_id,

        "campeonato": campeonato,

        "data": data_jogo,

        "time_casa": time_casa,

        "time_fora": time_fora,

        "escalação": escalação,

        "desfalques": desfalques,

        "transmissao": transmissao
    }
