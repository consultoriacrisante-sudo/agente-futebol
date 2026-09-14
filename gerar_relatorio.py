"""
gerar_relatorio.py

Monta o texto final do relatório, no formato Markdown que o Telegram
entende (enviar_telegram.py já manda com parse_mode="Markdown").

Segue o template definido no projeto:

⚽ JOGO
📺 Onde assistir
📋 Provável escalação (com confiança 🟢🟡🔴, se disponível)
🚑 Desfalques
❓ Dúvidas
📊 Confiança geral

Este arquivo só formata texto — não busca dados nem depende de API.
Por isso dá pra testar sozinho, sem internet.
"""


# ============================================================
# FORMATAR LISTA DE JOGADORES (com ou sem confiança)
# ============================================================

def formatar_lista_jogadores(jogadores) -> str:
    """
    Aceita duas formas de entrada:
    - lista simples de nomes: ["Fulano", "Ciclano"]
    - lista com confiança: [{"jogador": "Fulano", "emoji": "🟢"}, ...]
    """

    if not jogadores:
        return "_Escalação não disponível_"

    linhas = []

    for item in jogadores:

        if isinstance(item, dict):
            emoji = item.get("emoji", "")
            nome = item.get("jogador", "")
            linhas.append(f"{emoji} {nome}".strip())
        else:
            linhas.append(f"• {item}")

    return "\n".join(linhas)


# ============================================================
# FORMATAR DESFALQUES
# ============================================================

def formatar_desfalques(desfalques: list[dict]) -> str:

    if not desfalques:
        return "_Nenhum desfalque encontrado_"

    linhas = []

    for item in desfalques:
        jogador = item.get("jogador", "")
        motivo = item.get("motivo_pt", item.get("motivo", ""))
        linhas.append(f"• {jogador} — {motivo}")

    return "\n".join(linhas)


# ============================================================
# FORMATAR TRANSMISSÃO
# ============================================================

def formatar_transmissao(fontes_transmissao: list[dict]) -> str:
    """
    Espera itens no formato:
        {"canal": "YouTube", "tipo": "Gratuito", "url": "https://..."}
    """

    if not fontes_transmissao:
        return "_Transmissão não encontrada_"

    linhas = []

    for item in fontes_transmissao:
        canal = item.get("canal", "")
        tipo = item.get("tipo", "")
        url = item.get("url", "")

        if url:
            linhas.append(f"• [{canal}]({url}) — {tipo}")
        else:
            linhas.append(f"• {canal} — {tipo}")

    return "\n".join(linhas)


# ============================================================
# MONTAR RELATÓRIO COMPLETO
# ============================================================

def montar_relatorio(dados: dict) -> str:
    """
    dados esperado:
    {
        "campeonato": str,
        "time_casa": str,
        "time_fora": str,
        "data": str,
        "horario": str,
        "estadio": str,
        "transmissao": [ {canal, tipo, url}, ... ],
        "escalacao_casa": [ {jogador, emoji}, ... ] ou lista simples,
        "escalacao_fora": [ ... ],
        "desfalques_casa": [ {jogador, motivo_pt}, ... ],
        "desfalques_fora": [ ... ],
        "duvidas": [ "Nome (Time)", ... ],   # opcional
    }
    """

    partes = []

    # --------------------------------------------------------
    # CABEÇALHO DO JOGO
    # --------------------------------------------------------

    partes.append(
        f"⚽ *{dados['time_casa']} x {dados['time_fora']}*\n"
        f"🏆 {dados['campeonato']}\n"
        f"📅 {dados['data']}  ⏰ {dados['horario']} (Brasília)\n"
        f"🏟️ {dados.get('estadio', 'Não informado')}"
    )

    # --------------------------------------------------------
    # ONDE ASSISTIR
    # --------------------------------------------------------

    partes.append(
        "📺 *Onde assistir*\n" +
        formatar_transmissao(dados.get("transmissao", []))
    )

    # --------------------------------------------------------
    # ESCALAÇÕES
    # --------------------------------------------------------

    partes.append(
        f"📋 *Provável escalação — {dados['time_casa']}*\n" +
        formatar_lista_jogadores(dados.get("escalacao_casa", []))
    )

    partes.append(
        f"📋 *Provável escalação — {dados['time_fora']}*\n" +
        formatar_lista_jogadores(dados.get("escalacao_fora", []))
    )

    # --------------------------------------------------------
    # DESFALQUES
    # --------------------------------------------------------

    partes.append(
        f"🚑 *Desfalques — {dados['time_casa']}*\n" +
        formatar_desfalques(dados.get("desfalques_casa", []))
    )

    partes.append(
        f"🚑 *Desfalques — {dados['time_fora']}*\n" +
        formatar_desfalques(dados.get("desfalques_fora", []))
    )

    # --------------------------------------------------------
    # DÚVIDAS (opcional)
    # --------------------------------------------------------

    duvidas = dados.get("duvidas")

    if duvidas:
        linhas_duvidas = "\n".join(f"• {nome}" for nome in duvidas)
        partes.append(f"❓ *Dúvidas*\n{linhas_duvidas}")

    # --------------------------------------------------------
    # JUNTAR TUDO
    # --------------------------------------------------------

    return "\n\n".join(partes)


# ============================================================
# TESTE COM DADOS FICTÍCIOS (baseados no caso real Cruzeiro)
# ============================================================

if __name__ == "__main__":

    dados_teste = {
        "campeonato": "Copa do Brasil — Quartas de final",
        "time_casa": "Cruzeiro",
        "time_fora": "Atlético-MG",
        "data": "25/08/2026",
        "horario": "21:00",
        "estadio": "Mineirão — Belo Horizonte/MG",
        "transmissao": [
            {"canal": "SporTV", "tipo": "Pago (TV fechada)", "url": ""},
            {"canal": "Premiere", "tipo": "Pago (pay-per-view)", "url": ""},
        ],
        "escalacao_casa": [
            {"jogador": "Otávio", "emoji": "🟡"},
            {"jogador": "Fagner", "emoji": "🟡"},
            {"jogador": "Fabrício Bruno", "emoji": "🟡"},
            {"jogador": "Lucas Romero", "emoji": "🟡"},
            {"jogador": "Gerson", "emoji": "🟡"},
            {"jogador": "Kaio Jorge", "emoji": "🟡"},
        ],
        "escalacao_fora": [
            "Éverson", "Natanael", "Tressoldi", "Renan Lodi", "Bernard", "Cuello",
        ],
        "desfalques_casa": [
            {"jogador": "Luis Sinisterra", "motivo_pt": "Lesão"},
            {"jogador": "Gabriel Pec", "motivo_pt": "Lesão"},
        ],
        "desfalques_fora": [
            {"jogador": "Gustavo Scarpa", "motivo_pt": "Lesão muscular"},
        ],
        "duvidas": ["Patrick (Atlético-MG)"],
    }

    relatorio = montar_relatorio(dados_teste)

    print(relatorio)
    print()
    print("=" * 60)
    print(f"Tamanho do relatório: {len(relatorio)} caracteres")
    print(
        "(Limite do Telegram por mensagem: 4096 caracteres — "
        "dentro do limite se ficar abaixo disso)"
    )
