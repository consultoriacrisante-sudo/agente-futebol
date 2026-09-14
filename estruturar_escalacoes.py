import re


# ============================================================
# ESTRUTURAR DADOS DE ESCALAÇÃO
# ============================================================

def estruturar_escalacao(resultado):

    titulo = resultado.get("title", "")
    url = resultado.get("url", "")
    conteudo = resultado.get("content", "")

    texto = conteudo or ""

    titulo_minusculo = titulo.lower()
    texto_minusculo = texto.lower()

    # ========================================================
    # IDENTIFICAR ESCALAÇÃO CONFIRMADA
    # ========================================================

    palavras_confirmada = [
        "confirmed lineup",
        "confirmed lineups",
        "starting lineup confirmed",
        "starting lineups confirmed",
        "lineup confirmed",
        "lineups confirmed",
        "confirmed starting xi",
        "starting xi confirmed",
        "escalação confirmada",
        "escalações confirmadas",
        "escalação oficial",
        "escalações oficiais"
    ]

    confirmada = False

    for palavra in palavras_confirmada:

        if (
            palavra in titulo_minusculo
            or palavra in texto_minusculo
        ):
            confirmada = True
            break

    # ========================================================
    # IDENTIFICAR SE O TEXTO FALA APENAS DE PROVÁVEIS
    # ========================================================

    palavras_provavel = [
        "prováveis escalações",
        "provavel escalação",
        "prováveis escalações",
        "prováveis escalações",
        "predicted lineups",
        "predicted lineup",
        "expected lineup",
        "expected lineups",
        "possible lineup",
        "possible lineups",
        "projected lineup",
        "projected lineups"
    ]

    apenas_provavel = False

    encontrou_provavel = False

    for palavra in palavras_provavel:

        if palavra in titulo_minusculo:
            encontrou_provavel = True
            break

    # Se não há confirmação e o título é claramente de previsão,
    # não devemos tratar como escalação confirmada.

    if encontrou_provavel and not confirmada:

        apenas_provavel = True

    # ========================================================
    # IDENTIFICAR FORMAÇÃO
    # ========================================================

    formacao = None

    # Procurar formações somente em padrões razoavelmente válidos.
    #
    # Exemplos:
    # 4-3-3
    # 4-2-3-1
    # 3-5-2
    # 4-4-2

    padrao_formacao = re.compile(
        r"\b([3-5])-(\d)-(\d)(?:-(\d))?\b"
    )

    formacoes = padrao_formacao.findall(texto)

    if formacoes:

        for formacao_encontrada in formacoes:

            partes = [
                parte
                for parte in formacao_encontrada
                if parte
            ]

            if len(partes) >= 3:

                formacao = "-".join(partes)

                break

    # ========================================================
    # SE NÃO FOR CONFIRMADA
    # ========================================================

    if not confirmada:

        formacao = None

    # ========================================================
    # RETORNAR ESTRUTURA
    # ========================================================

    return {
        "titulo": titulo,
        "url": url,
        "confirmada": confirmada,
        "apenas_provavel": apenas_provavel,
        "formacao": formacao,
        "conteudo": conteudo
    }
