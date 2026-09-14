"""
rodar_agente.py

SCRIPT PRINCIPAL — roda o agente-futebol de ponta a ponta, sob demanda.

Fluxo:
  1. Busca os jogos do dia (das competições monitoradas)
  2. Você escolhe qual jogo quer o relatório
  3. Busca fontes de escalação (Tavily) e extrai jogadores de TODAS elas
  4. Aplica normalização de nomes + sistema de confiança (🟢🟡🔴)
  5. Busca desfalques (API-Football)
  6. Busca onde assistir (Tavily, fontes brasileiras prioritárias)
  7. Monta o relatório formatado
  8. Envia para o Telegram

Uso:
    python rodar_agente.py
"""

from buscar_jogos import buscar_jogos, filtrar_jogos
from formatar_jogos import formatar_jogo
from buscar_escalacoes import buscar_escalacoes
from estruturar_escalacoes import estruturar_escalacao
from extrair_lineups import extrair_lineup
from normalizar_nomes import agrupar_jogadores  # usado indiretamente via sistema_confianca
from sistema_confianca import calcular_confianca_time
from desfalques import estruturar_desfalques
from pesquisar_transmissoes import pesquisar_transmissao
from gerar_relatorio import montar_relatorio
from enviar_telegram import enviar_mensagem_telegram


# ============================================================
# ESCOLHER O JOGO
# ============================================================

def escolher_jogo(jogos_formatados: list[dict]) -> dict:

    print()
    print("JOGOS DE HOJE")
    print("=" * 60)

    for indice, jogo in enumerate(jogos_formatados, start=1):
        print(
            f'{indice}. {jogo["time_casa"]} x {jogo["time_fora"]} '
            f'— {jogo["campeonato"]} — {jogo["horario"]}'
        )

    print()
    escolha = input("Digite o número do jogo desejado: ").strip()

    try:
        indice_escolhido = int(escolha) - 1
        return jogos_formatados[indice_escolhido]
    except (ValueError, IndexError):
        print("Escolha inválida. Usando o primeiro jogo da lista.")
        return jogos_formatados[0]


# ============================================================
# MONTAR FONTES DE ESCALAÇÃO POR TIME (para o sistema de confiança)
# ============================================================

def montar_fontes_por_time(fontes_brutas, time_casa, time_fora):

    fontes_casa = []
    fontes_fora = []

    for fonte in fontes_brutas:

        estrutura = estruturar_escalacao(fonte)
        extracao = extrair_lineup(fonte, time_casa, time_fora)

        if extracao["jogadores_casa"]:
            fontes_casa.append({
                "url": fonte.get("url", ""),
                "confirmada": estrutura.get("confirmada", False),
                "jogadores": extracao["jogadores_casa"],
            })

        if extracao["jogadores_fora"]:
            fontes_fora.append({
                "url": fonte.get("url", ""),
                "confirmada": estrutura.get("confirmada", False),
                "jogadores": extracao["jogadores_fora"],
            })

    return fontes_casa, fontes_fora


# ============================================================
# SEPARAR DESFALQUES POR TIME
# ============================================================

def separar_desfalques_por_time(desfalques, time_casa, time_fora):

    desfalques_casa = [d for d in desfalques if d["time"] == time_casa]
    desfalques_fora = [d for d in desfalques if d["time"] == time_fora]

    return desfalques_casa, desfalques_fora


# ============================================================
# MONTAR TRANSMISSÃO NO FORMATO DO RELATÓRIO
# ============================================================

def montar_transmissao_formatada(resultado_pesquisa):

    transmissao = []

    for item in resultado_pesquisa["resultados"]:

        titulo = item.get("titulo", "")
        titulo_curto = titulo[:60] + "..." if len(titulo) > 60 else titulo

        transmissao.append({
            "canal": item.get("fonte", ""),
            "tipo": titulo_curto,
            "url": item.get("url", ""),
        })

    return transmissao


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():

    print()
    print("=" * 60)
    print("AGENTE FUTEBOL")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. BUSCAR JOGOS DO DIA
    # --------------------------------------------------------

    jogos_brutos = filtrar_jogos(buscar_jogos())

    if not jogos_brutos:
        print()
        print("Nenhum jogo encontrado hoje nas competições monitoradas.")
        return

    jogos_formatados = [formatar_jogo(jogo) for jogo in jogos_brutos]

    # --------------------------------------------------------
    # 2. ESCOLHER O JOGO
    # --------------------------------------------------------

    jogo = escolher_jogo(jogos_formatados)

    time_casa = jogo["time_casa"]
    time_fora = jogo["time_fora"]

    print()
    print(f"Gerando relatório: {time_casa} x {time_fora}")
    print("=" * 60)

    # --------------------------------------------------------
    # 3. BUSCAR E PROCESSAR ESCALAÇÕES (TODAS AS FONTES)
    # --------------------------------------------------------

    print()
    print("Buscando escalações...")

    fontes_brutas = buscar_escalacoes(
        time_casa, time_fora, jogo["campeonato"], jogo["data"]
    )

    fontes_casa, fontes_fora = montar_fontes_por_time(
        fontes_brutas, time_casa, time_fora
    )

    escalacao_casa = calcular_confianca_time(fontes_casa)
    escalacao_fora = calcular_confianca_time(fontes_fora)

    # --------------------------------------------------------
    # 4. BUSCAR DESFALQUES
    # --------------------------------------------------------

    print("Buscando desfalques...")

    resultado_desfalques = estruturar_desfalques(jogo["fixture_id"])

    desfalques_casa, desfalques_fora = separar_desfalques_por_time(
        resultado_desfalques["desfalques"], time_casa, time_fora
    )

    # --------------------------------------------------------
    # 5. BUSCAR TRANSMISSÃO
    # --------------------------------------------------------

    print("Buscando onde assistir...")

    resultado_transmissao = pesquisar_transmissao(jogo)

    transmissao = montar_transmissao_formatada(resultado_transmissao)

    # --------------------------------------------------------
    # 6. MONTAR RELATÓRIO
    # --------------------------------------------------------

    print("Montando relatório...")

    dados_relatorio = {
        "campeonato": jogo["campeonato"],
        "time_casa": time_casa,
        "time_fora": time_fora,
        "data": jogo["data"],
        "horario": jogo["horario"],
        "estadio": jogo["estadio"],
        "transmissao": transmissao,
        "escalacao_casa": escalacao_casa,
        "escalacao_fora": escalacao_fora,
        "desfalques_casa": desfalques_casa,
        "desfalques_fora": desfalques_fora,
    }

    relatorio = montar_relatorio(dados_relatorio)

    print()
    print("=" * 60)
    print("RELATÓRIO GERADO")
    print("=" * 60)
    print()
    print(relatorio)

    # --------------------------------------------------------
    # 7. ENVIAR PARA O TELEGRAM
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("Enviando para o Telegram...")

    enviar_mensagem_telegram(relatorio)


if __name__ == "__main__":
    main()
