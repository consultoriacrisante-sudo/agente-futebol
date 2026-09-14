"""
relatorio.py

Monta o texto final do relatório de um jogo, pronto para enviar ao Telegram.

⚠️ ATENÇÃO — SUPOSIÇÕES ASSUMIDAS NESTE ARQUIVO:

Como ainda não tínhamos um exemplo real do dicionário devolvido por
`montar_dados_jogo`, este código foi escrito assumindo os seguintes formatos
(baseados na descrição dos outros módulos):

1. dados_jogo["escalação"] (vindo de montar_escalacao_final.py):
   {
       "confirmada": True/False,
       "formação": "4-3-3",
       "fonte": "https://...",
       "pontuação": 850,
       "jogadores": {
           "time_casa": ["Jogador 1", "Jogador 2", ...],
           "time_fora": ["Jogador 1", "Jogador 2", ...]
       }
   }

2. dados_jogo["desfalques"] (vindo de desfalques.py / buscar_desfalques.py):
   {
       "total": 3,
       "desfalques": [
           {"jogador": "Nome", "time": "Time X", "status": "Suspenso", "motivo": "Cartão vermelho"},
           ...
       ]
   }

3. dados_jogo["transmissao"] (vindo de pesquisar_transmissoes.py):
   {
       "jogo": {...},
       "termo": "...",
       "resultados": [
           {"fonte": "GE", "titulo": "...", "url": "...", "descricao": "...", "score": 0.9},
           ...
       ]
   }

SE DER ERRO (ex: KeyError, ou o texto sair com "não identificado" demais):
Rode o pipeline com um jogo real, copie o dicionário completo devolvido por
`montar_dados_jogo` e me mande — eu ajusto os nomes dos campos em 1 minuto,
sem precisar reescrever o arquivo inteiro.
"""

from dados_jogo import separar_data_horario


# ============================================================
# SEÇÃO: CABEÇALHO
# ============================================================

def formatar_cabecalho(dados_jogo):

    time_casa = dados_jogo.get("time_casa", "Time Casa")
    time_fora = dados_jogo.get("time_fora", "Time Visitante")
    campeonato = dados_jogo.get("campeonato", "")

    data_str, horario_str = separar_data_horario(
        dados_jogo.get("data", "")
    )

    linhas = [
        f"⚽ *{time_casa} x {time_fora}*"
    ]

    if campeonato:
        linhas.append(f"🏆 {campeonato}")

    if data_str:
        linhas.append(f"📅 {data_str} — 🕐 {horario_str}")

    return "\n".join(linhas)


# ============================================================
# SEÇÃO: ESCALAÇÃO
# ============================================================

def formatar_secao_escalacao(escalacao):

    if not escalacao:
        return "📋 *Escalações*\nInformação não disponível."

    confirmada = escalacao.get("confirmada", False)

    formacao = escalacao.get("formação") or escalacao.get("formacao") or "não identificada"

    status_label = "✅ Confirmada" if confirmada else "❓ Provável"

    linhas = [f"📋 *Escalações* ({status_label} — {formacao})"]

    jogadores = escalacao.get("jogadores", {})

    # Suporta tanto {"time_casa": [...], "time_fora": [...]} quanto uma lista única
    if isinstance(jogadores, dict):

        nomes_exibicao = {
            "time_casa": "Casa",
            "time_fora": "Visitante"
        }

        for chave, rotulo in nomes_exibicao.items():

            lista = jogadores.get(chave, [])

            if lista:
                linhas.append(f"\n*{rotulo}:*")
                for jogador in lista:
                    linhas.append(f"• {jogador}")

    elif isinstance(jogadores, list) and jogadores:

        for jogador in jogadores:
            linhas.append(f"• {jogador}")

    else:
        linhas.append("Jogadores não disponíveis.")

    return "\n".join(linhas)


# ============================================================
# SEÇÃO: DESFALQUES
# ============================================================

def formatar_secao_desfalques(desfalques):

    if not desfalques:
        return "🚑 *Desfalques*\nNenhuma informação disponível."

    total = desfalques.get("total", 0)

    lista = desfalques.get("desfalques", [])

    if total == 0 or not lista:
        return "🚑 *Desfalques*\nNenhum desfalque relevante encontrado."

    icones_status = {
        "Suspenso": "🟥",
        "Fora": "🚑",
        "Dúvida": "❓",
        "Indisponível": "⛔"
    }

    linhas = ["🚑 *Desfalques*"]

    for item in lista:

        jogador = item.get("jogador", "Jogador não identificado")

        time = item.get("time", "")

        status = item.get("status", "")

        motivo = item.get("motivo", "")

        icone = icones_status.get(status, "•")

        linha = f"{icone} {jogador}"

        if time:
            linha += f" ({time})"

        if status:
            linha += f" — {status}"

        if motivo:
            linha += f": {motivo}"

        linhas.append(linha)

    return "\n".join(linhas)


# ============================================================
# SEÇÃO: TRANSMISSÃO
# ============================================================

def formatar_secao_transmissao(transmissao):

    if not transmissao:
        return "📺 *Onde assistir*\nNão encontramos informação de transmissão."

    resultados = transmissao.get("resultados", [])

    if not resultados:
        return "📺 *Onde assistir*\nNão encontramos informação de transmissão."

    melhor = resultados[0]

    linhas = ["📺 *Onde assistir*"]

    fonte = melhor.get("fonte", "Fonte")
    titulo = melhor.get("titulo", "")
    url = melhor.get("url", "")

    linhas.append(f"{fonte}: {titulo}")

    if url:
        linhas.append(url)

    return "\n".join(linhas)


# ============================================================
# MONTAR RELATÓRIO COMPLETO DE UM JOGO
# ============================================================

def montar_relatorio(dados_jogo):

    partes = [
        formatar_cabecalho(dados_jogo),
        "",
        formatar_secao_escalacao(dados_jogo.get("escalação", {})),
        "",
        formatar_secao_desfalques(dados_jogo.get("desfalques", {})),
        "",
        formatar_secao_transmissao(dados_jogo.get("transmissao", {}))
    ]

    return "\n".join(partes)
