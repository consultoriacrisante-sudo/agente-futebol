import re


# ============================================================
# NORMALIZAR TEXTO
# ============================================================

def normalizar(texto):

    if not texto:
        return ""

    texto = texto.replace("\n", " ")

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()


# ============================================================
# LIMPAR NOME
# ============================================================

def limpar_nome(nome):

    if not nome:
        return ""

    nome = nome.strip()

    nome = re.sub(
        r"^\d+\.\s*",
        "",
        nome
    )

    nome = nome.rstrip(
        ".,;:[]"
    )

    return nome.strip()


# ============================================================
# VALIDAR NOME
# ============================================================

def nome_valido(nome):

    if not nome:
        return False

    if len(nome) < 3:
        return False

    if len(nome) > 45:
        return False

    lixo = [

        "probable lineup",
        "predicted lineup",
        "expected lineup",
        "possible lineup",

        "key matchup",
        "matchup factors",
        "both teams",

        "protected by",
        "back line",
        "goalkeeper",
        "formation",
        "setup",
        "double pivot",
        "midfield",
        "attacking midfield",
        "lone striker",
        "providing protection",

        "august",
        "september",
        "october",
        "november",
        "december",
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july"
    ]

    nome_lower = nome.lower()

    for palavra in lixo:

        if palavra in nome_lower:

            return False

    return True


# ============================================================
# CORRIGIR NOMES
# ============================================================

def corrigir_nome(nome):

    correcoes = {

        "Igor":
            "Igor Paixão",

        "Hojbjerg":
            "Pierre-Emile Højbjerg",

        "Pierre-Emile Hojbjerg":
            "Pierre-Emile Højbjerg",

        "Filip Jorgensen":
            "Filip Jörgensen",

        "Ismael Doukoure":
            "Ismaël Doukouré",

        "Sam Amo Ameyaw":
            "Sam Amo-Ameyaw",

        "Samir El Mourabet":
            "Samir El Mourabet"
    }

    return correcoes.get(
        nome,
        nome
    )


# ============================================================
# REMOVER DUPLICADOS
# ============================================================

def remover_duplicados(jogadores):

    resultado = []

    nomes_normalizados = set()

    for jogador in jogadores:

        jogador = limpar_nome(
            jogador
        )

        jogador = corrigir_nome(
            jogador
        )

        chave = jogador.lower()

        if chave in nomes_normalizados:
            continue

        if not nome_valido(jogador):
            continue

        nomes_normalizados.add(
            chave
        )

        resultado.append(
            jogador
        )

    return resultado


# ============================================================
# LOCALIZAR CABEÇALHO
# ============================================================

def localizar_cabecalho(
    texto,
    time
):

    padrao = re.compile(

        rf"{re.escape(time)}\s+"
        rf"(?:probable|predicted|expected|possible)"
        rf"\s+line[\s-]?up\s*:",

        re.IGNORECASE
    )

    return padrao.search(
        texto
    )


# ============================================================
# EXTRAIR BLOCO GENÉRICO
# ============================================================

def extrair_bloco(
    texto,
    time_atual,
    time_proximo=None
):

    texto = normalizar(
        texto
    )

    inicio = localizar_cabecalho(
        texto,
        time_atual
    )

    if not inicio:

        return None

    inicio_pos = inicio.end()

    fim_pos = len(
        texto
    )

    if time_proximo:

        proximo = localizar_cabecalho(
            texto,
            time_proximo
        )

        if proximo:

            fim_pos = proximo.start()

    bloco = texto[
        inicio_pos:fim_pos
    ]

    marcadores = [

        "[...]",
        "##",
        "Key Matchup",
        "Key Factors",
        "Matchup Factors",
        "Both teams",
        "The primary",
        "Place your bets"
    ]

    for marcador in marcadores:

        posicao = bloco.find(
            marcador
        )

        if posicao != -1:

            bloco = bloco[
                :posicao
            ]

    return bloco.strip()


# ============================================================
# LIMPAR MARCADORES
# ============================================================

def limpar_marcadores(
    texto
):

    texto = re.sub(

        r"\s+\d+\.\s*"
        r"(GK|DEF|MID|FWD)\s*:",

        "|",

        texto,

        flags=re.IGNORECASE
    )

    texto = re.sub(

        r"\d+\.\s*"
        r"(GK|DEF|MID|FWD)\s*:",

        "|",

        texto,

        flags=re.IGNORECASE
    )

    texto = re.sub(

        r"\b"
        r"(GK|DEF|MID|FWD)"
        r"\s*:",

        "|",

        texto,

        flags=re.IGNORECASE
    )

    return texto


# ============================================================
# EXTRAIR JOGADORES DE BLOCO GENÉRICO
# ============================================================

def extrair_jogadores(
    bloco
):

    if not bloco:

        return []

    bloco = limpar_marcadores(
        bloco
    )

    jogadores = []

    grupos = bloco.split(
        "|"
    )

    for grupo in grupos:

        grupo = grupo.strip()

        if not grupo:
            continue

        grupo = re.sub(
            r"^\d+\.\s*",
            "",
            grupo
        )

        nomes = grupo.split(
            ","
        )

        for nome in nomes:

            nome = limpar_nome(
                nome
            )

            nome = corrigir_nome(
                nome
            )

            if nome_valido(nome):

                jogadores.append(
                    nome
                )

    return remover_duplicados(
        jogadores
    )


# ============================================================
# EXTRAIR WHO SCORED - MARSEILLE
# ============================================================

def extrair_whoscored_marseille(
    texto
):

    jogadores = []

    padrao = re.search(

        r"Marseille starting lineup:\s*"
        r"(.*?)(?:\.\.\.|\n|$)",

        texto,

        re.IGNORECASE
    )

    if not padrao:

        return []

    linha = padrao.group(
        1
    )

    partes = linha.split(
        ","
    )

    for parte in partes:

        nome = limpar_nome(
            parte
        )

        nome = corrigir_nome(
            nome
        )

        if nome_valido(nome):

            jogadores.append(
                nome
            )

    return remover_duplicados(
        jogadores
    )[:11]


# ============================================================
# EXTRAIR WHO SCORED - STRASBOURG
# ============================================================

def extrair_whoscored_strasbourg(
    texto
):

    jogadores = []

    # ========================================================
    # LOCALIZAR SEÇÃO STRASBOURG
    # ========================================================

    padrao_secao = re.search(

        r"###\s+Strasbourg"
        r"(.*?)(?=\n###|\Z)",

        texto,

        re.IGNORECASE |
        re.DOTALL
    )

    if not padrao_secao:

        return []

    bloco = padrao_secao.group(
        1
    )

    # ========================================================
    # GOLEIRO
    #
    # goalkeeper Filip Jörgensen protected
    # ========================================================

    padrao = re.search(

        r"goalkeeper\s+"
        r"([A-ZÀ-ÿ][A-Za-zÀ-ÿ'’\-]+"
        r"(?:\s+[A-ZÀ-ÿ][A-Za-zÀ-ÿ'’\-]+)*)"
        r"\s+protected",

        bloco,

        re.IGNORECASE
    )

    if padrao:

        nome = limpar_nome(
            padrao.group(1)
        )

        nome = corrigir_nome(
            nome
        )

        if nome_valido(nome):

            jogadores.append(
                nome
            )

    # ========================================================
    # DEFESA
    #
    # back line of Genesis Antwi,
    # Andrew Omobamidele,
    # Lucas Høgsberg and Guéla Doué.
    # ========================================================

    padrao = re.search(

        r"back line of\s+"
        r"(.+?)"
        r"\.\s+Diogo Sousa",

        bloco,

        re.IGNORECASE |
        re.DOTALL
    )

    if padrao:

        defesa = padrao.group(
            1
        )

        defesa = re.sub(

            r"\s+and\s+",

            ", ",

            defesa,

            flags=re.IGNORECASE
        )

        for nome in defesa.split(","):

            nome = limpar_nome(
                nome
            )

            nome = corrigir_nome(
                nome
            )

            if nome_valido(nome):

                jogadores.append(
                    nome
                )

    # ========================================================
    # MEIO
    #
    # Diogo Sousa and Samir El Mourabet
    # form the double pivot
    # ========================================================

    padrao = re.search(

        r"(Diogo Sousa)"
        r"\s+and\s+"
        r"([A-ZÀ-ÿ][A-Za-zÀ-ÿ'’\-]+"
        r"(?:\s+[A-ZÀ-ÿ][A-Za-zÀ-ÿ'’\-]+)*)"
        r"\s+form the double pivot",

        bloco,

        re.IGNORECASE
    )

    if padrao:

        nome1 = limpar_nome(
            padrao.group(1)
        )

        nome2 = limpar_nome(
            padrao.group(2)
        )

        nome1 = corrigir_nome(
            nome1
        )

        nome2 = corrigir_nome(
            nome2
        )

        if nome_valido(nome1):

            jogadores.append(
                nome1
            )

        if nome_valido(nome2):

            jogadores.append(
                nome2
            )

    # ========================================================
    # TRIO OFENSIVO
    #
    # trio of Gessime Yassine,
    # Sam Amo-Ameyaw and Sebastian Nanasi
    # behind lone striker
    # ========================================================

    padrao = re.search(

        r"trio of\s+"
        r"(.+?)"
        r"\s+behind lone striker",

        bloco,

        re.IGNORECASE |
        re.DOTALL
    )

    if padrao:

        trio = padrao.group(
            1
        )

        trio = re.sub(

            r"\s+and\s+",

            ", ",

            trio,

            flags=re.IGNORECASE
        )

        for nome in trio.split(","):

            nome = limpar_nome(
                nome
            )

            nome = corrigir_nome(
                nome
            )

            if nome_valido(nome):

                jogadores.append(
                    nome
                )

    # ========================================================
    # ATACANTE
    #
    # behind lone striker Sékou Mara
    # ========================================================

    padrao = re.search(

        r"behind lone striker\s+"
        r"([A-ZÀ-ÿ][A-Za-zÀ-ÿ'’\-]+"
        r"(?:\s+[A-ZÀ-ÿ][A-Za-zÀ-ÿ'’\-]+)*)",

        bloco,

        re.IGNORECASE
    )

    if padrao:

        nome = limpar_nome(
            padrao.group(1)
        )

        nome = corrigir_nome(
            nome
        )

        if nome_valido(nome):

            jogadores.append(
                nome
            )

    # ========================================================
    # LIMPEZA FINAL
    # ========================================================

    jogadores = remover_duplicados(
        jogadores
    )

    return jogadores[:11]


# ============================================================
# EXTRAIR WHO SCORED
# ============================================================

def extrair_whoscored(
    texto,
    time_casa,
    time_fora
):

    jogadores_casa = []
    jogadores_fora = []

    # ========================================================
    # MARSEILLE
    # ========================================================

    if time_casa.lower() == "marseille":

        jogadores_casa = (
            extrair_whoscored_marseille(
                texto
            )
        )

    elif time_fora.lower() == "marseille":

        jogadores_fora = (
            extrair_whoscored_marseille(
                texto
            )
        )

    # ========================================================
    # STRASBOURG
    # ========================================================

    if time_casa.lower() == "strasbourg":

        jogadores_casa = (
            extrair_whoscored_strasbourg(
                texto
            )
        )

    elif time_fora.lower() == "strasbourg":

        jogadores_fora = (
            extrair_whoscored_strasbourg(
                texto
            )
        )

    return {

        "jogadores_casa":
            jogadores_casa,

        "jogadores_fora":
            jogadores_fora
    }


# ============================================================
# EXTRAIR LINEUP GENÉRICO
# ============================================================

def extrair_lineup_generico(
    texto,
    time_casa,
    time_fora
):

    bloco_casa = extrair_bloco(
        texto,
        time_casa,
        time_fora
    )

    bloco_fora = extrair_bloco(
        texto,
        time_fora,
        None
    )

    jogadores_casa = extrair_jogadores(
        bloco_casa
    )

    jogadores_fora = extrair_jogadores(
        bloco_fora
    )

    return {

        "jogadores_casa":
            jogadores_casa,

        "jogadores_fora":
            jogadores_fora
    }

# ============================================================
# EXTRAIR LINEUP 365SCORES
# ============================================================

def extrair_365scores(
    texto,
    time_casa,
    time_fora
):

    jogadores_casa = []
    jogadores_fora = []

    texto_lower = texto.lower()

    # ========================================================
    # LOCALIZAR TIMES
    # ========================================================

    pos_casa = texto_lower.find(
        "home team:"
    )

    pos_fora = texto_lower.find(
        "away team:"
    )

    # ========================================================
    # SE NÃO ENCONTRAR A ESTRUTURA
    # ========================================================

    if pos_casa == -1 or pos_fora == -1:

        return {
            "jogadores_casa": [],
            "jogadores_fora": []
        }

    # ========================================================
    # SEPARAR BLOCOS
    # ========================================================

    if pos_casa < pos_fora:

        bloco_casa = texto[
            pos_casa:pos_fora
        ]

        bloco_fora = texto[
            pos_fora:
        ]

    else:

        bloco_fora = texto[
            pos_fora:pos_casa
        ]

        bloco_casa = texto[
            pos_casa:
        ]

    # ========================================================
    # EXTRAIR JOGADORES
    # ========================================================

    jogadores_casa = (
        extrair_jogadores_estruturados(
            bloco_casa
        )
    )

    jogadores_fora = (
        extrair_jogadores_estruturados(
            bloco_fora
        )
    )

    return {

        "jogadores_casa":
            jogadores_casa[:11],

        "jogadores_fora":
            jogadores_fora[:11]
    }


# ============================================================
# EXTRAIR JOGADORES DE BLOCO ESTRUTURADO
# ============================================================

def extrair_jogadores_estruturados(
    bloco
):

    if not bloco:

        return []

    jogadores = []

    # ========================================================
    # GOLEIRO
    # ========================================================

    padrao = re.search(

        r"Goalkeeper:\s*"
        r"([^.\n]+)",

        bloco,

        re.IGNORECASE
    )

    if padrao:

        nome = padrao.group(1)

        nome = limpar_nome(
            nome
        )

        nome = corrigir_nome(
            nome
        )

        if nome_valido(nome):

            jogadores.append(
                nome
            )

    # ========================================================
    # DEFENSORES
    # ========================================================

    padrao = re.search(

        r"Defenders?:\s*"
        r"([^.\n]+)",

        bloco,

        re.IGNORECASE
    )

    if padrao:

        extracao = padrao.group(1)

        extracao = re.sub(

            r"\s+and\s+",

            ", ",

            extracao,

            flags=re.IGNORECASE
        )

        for nome in extracao.split(","):

            nome = limpar_nome(
                nome
            )

            nome = corrigir_nome(
                nome
            )

            if nome_valido(nome):

                jogadores.append(
                    nome
                )

    # ========================================================
    # MEIO-CAMPISTAS
    # ========================================================

    padrao = re.search(

        r"Midfielders?:\s*"
        r"([^.\n]+)",

        bloco,

        re.IGNORECASE
    )

    if padrao:

        extracao = padrao.group(1)

        extracao = re.sub(

            r"\s+and\s+",

            ", ",

            extracao,

            flags=re.IGNORECASE
        )

        for nome in extracao.split(","):

            nome = limpar_nome(
                nome
            )

            nome = corrigir_nome(
                nome
            )

            if nome_valido(nome):

                jogadores.append(
                    nome
                )

    # ========================================================
    # ATACANTES
    # ========================================================

    padrao = re.search(

        r"(?:Forwards?|Attackers?):\s*"
        r"([^.\n]+)",

        bloco,

        re.IGNORECASE
    )

    if padrao:

        extracao = padrao.group(1)

        extracao = re.sub(

            r"\s+and\s+",

            ", ",

            extracao,

            flags=re.IGNORECASE
        )

        for nome in extracao.split(","):

            nome = limpar_nome(
                nome
            )

            nome = corrigir_nome(
                nome
            )

            if nome_valido(nome):

                jogadores.append(
                    nome
                )

    # ========================================================
    # LIMPEZA FINAL
    # ========================================================

    return remover_duplicados(
        jogadores
    )
# ============================================================
# EXTRAIR LINEUP PRINCIPAL
# ============================================================

def extrair_lineup(
    resultado,
    time_casa,
    time_fora
):

    titulo = resultado.get(
        "title",
        ""
    )

    conteudo = resultado.get(
        "content",
        ""
    )

    url = resultado.get(
        "url",
        ""
    )

    texto = (
        f"{titulo}\n{conteudo}"
    )

    # ========================================================
    # WHO SCORED
    #
    # NÃO USAR O PARSER GENÉRICO.
    # ========================================================

    if "whoscored.com" in url.lower():

        resultado_whoscored = (
            extrair_whoscored(
                texto,
                time_casa,
                time_fora
            )
        )

        jogadores_casa = (
            resultado_whoscored[
                "jogadores_casa"
            ]
        )

        jogadores_fora = (
            resultado_whoscored[
                "jogadores_fora"
            ]
        )

    else:

        resultado_generico = (
            extrair_lineup_generico(
                texto,
                time_casa,
                time_fora
            )
        )

        jogadores_casa = (
            resultado_generico[
                "jogadores_casa"
            ]
        )

        jogadores_fora = (
            resultado_generico[
                "jogadores_fora"
            ]
        )

    # ========================================================
    # RESULTADO
    # ========================================================

    return {

        "time_casa":
            time_casa,

        "time_fora":
            time_fora,

        "jogadores_casa":
            jogadores_casa,

        "jogadores_fora":
            jogadores_fora,

        "total_casa":
            len(jogadores_casa),

        "total_fora":
            len(jogadores_fora),

        "titulo":
            titulo,

        "url":
            url
    }
