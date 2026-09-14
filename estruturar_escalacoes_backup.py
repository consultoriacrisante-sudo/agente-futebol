import re


# ============================================================
# ESTRUTURAR DADOS DE ESCALAÇÃO
# ============================================================

def estruturar_escalacao(resultado):

    titulo = resultado.get("title", "")
    url = resultado.get("url", "")
    conteudo = resultado.get("content", "")

    texto = conteudo

    # ========================================================
    # IDENTIFICAR SE É ESCALAÇÃO CONFIRMADA
    # ========================================================

    confirmada = False

    palavras_confirmada = [
        "confirmed lineup",
        "confirmed lineups",
        "starting lineup",
        "starting xi",
        "lineup confirmed",
        "escalação confirmada",
        "escalações confirmadas"
    ]

    texto_minusculo = texto.lower()
    titulo_minusculo = titulo.lower()

    for palavra in palavras_confirmada:

        if palavra in texto_minusculo or palavra in titulo_minusculo:
            confirmada = True
            break

    # ========================================================
    # IDENTIFICAR FORMAÇÃO
    # ========================================================

    formacoes = re.findall(
        r"\b\d-\d(?:-\d)?(?:-\d)?\b",
        texto
    )

    formacao = None

    if formacoes:
        formacao = formacoes[0]

    # ========================================================
    # RETORNAR DADOS ESTRUTURADOS
    # ========================================================

    return {
        "titulo": titulo,
        "url": url,
        "confirmada": confirmada,
        "formacao": formacao,
        "conteudo": conteudo
    }
