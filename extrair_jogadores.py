import re


# ============================================================
# LIMPAR NOME DO JOGADOR
# ============================================================

def limpar_jogador(nome):

    nome = nome.strip()

    # Remover numeração
    nome = re.sub(
        r"^\s*\d+\.\s*",
        "",
        nome
    )

    # Remover posições
    nome = re.sub(
        r"^(GK|DEF|MID|FWD)\s*:\s*",
        "",
        nome,
        flags=re.IGNORECASE
    )

    # Remover pontuação nas extremidades
    nome = nome.strip(
        " .,:;[]()"
    )

    return nome.strip()


# ============================================================
# VALIDAR CANDIDATO
# ============================================================

def jogador_valido(nome):

    nome = nome.strip()

    if not nome:
        return False

    palavras_ignoradas = [
        "marseille",
        "strasbourg",
        "probable lineup",
        "probable line-up",
        "expected lineup",
        "expected line-up",
        "predicted lineup",
        "predicted line-up",
        "projected lineup",
        "projected line-up",
        "key matchup factors",
        "formation",
        "coach",
        "manager",
        "august 21",
        "2026"
    ]

    nome_lower = nome.lower()

    for palavra in palavras_ignoradas:

        if nome_lower == palavra:
            return False

    # Não aceitar frases muito longas
    if len(nome.split()) > 6:
        return False

    # Não aceitar números isolados
    if nome.isdigit():
        return False

    return True


# ============================================================
# ADICIONAR JOGADOR
# ============================================================

def adicionar_jogador(lista, nome):

    nome = limpar_jogador(nome)

    if jogador_valido(nome):

        lista.append(nome)


# ============================================================
# EXTRAIR BLOCO DE TIME
# ============================================================

def extrair_bloco_time(
    texto,
    time
):

    padroes = [

        # Marseille probable lineup:
        rf"{re.escape(time)}\s+probable\s+lineup\s*:\s*(.*?)(?={re.escape('Marseille' if time.lower() == 'strasbourg' else 'Strasbourg')}\s+(?:probable|expected|predicted|projected)\s+lineup\s*:|$)",

        # Marseille expected lineup:
        rf"{re.escape(time)}\s+expected\s+lineup\s*:\s*(.*?)(?={re.escape('Marseille' if time.lower() == 'strasbourg' else 'Strasbourg')}\s+(?:probable|expected|predicted|projected)\s+lineup\s*:|$)",

        # Marseille predicted lineup:
        rf"{re.escape(time)}\s+predicted\s+lineup\s*:\s*(.*?)(?={re.escape('Marseille' if time.lower() == 'strasbourg' else 'Strasbourg')}\s+(?:probable|expected|predicted|projected)\s+lineup\s*:|$)"
    ]

    for padrao in padroes:

        resultado = re.search(
            padrao,
            texto,
            re.IGNORECASE
        )

        if resultado:

            return resultado.group(1).strip()

    return ""


# ============================================================
# EXTRAIR FORMATO GK / DEF / MID / FWD
# ============================================================

def extrair_posicoes(bloco):

    jogadores = []

    # --------------------------------------------------------
    # GK
    # --------------------------------------------------------

    padrao = re.search(
        r"GK\s*:\s*(.*?)(?=\s+\d+\.\s*DEF\s*:|\s+DEF\s*:|$)",
        bloco,
        re.IGNORECASE
    )

    if padrao:

        adicionar_jogador(
            jogadores,
            padrao.group(1)
        )

    # --------------------------------------------------------
    # DEF
    # --------------------------------------------------------

    padrao = re.search(
        r"DEF\s*:\s*(.*?)(?=\s+\d+\.\s*MID\s*:|\s+MID\s*:|$)",
        bloco,
        re.IGNORECASE
    )

    if padrao:

        texto = padrao.group(1)

        texto = re.sub(
            r"\s+\d+\.\s*",
            ", ",
            texto
        )

        partes = re.split(
            r",|\s+e\s+",
            texto
        )

        for parte in partes:

            adicionar_jogador(
                jogadores,
                parte
            )

    # --------------------------------------------------------
    # MID
    # --------------------------------------------------------

    padrao = re.search(
        r"MID\s*:\s*(.*?)(?=\s+\d+\.\s*FWD\s*:|\s+FWD\s*:|$)",
        bloco,
        re.IGNORECASE
    )

    if padrao:

        texto = padrao.group(1)

        texto = re.sub(
            r"\s+\d+\.\s*",
            ", ",
            texto
        )

        partes = re.split(
            r",|\s+e\s+",
            texto
        )

        for parte in partes:

            adicionar_jogador(
                jogadores,
                parte
            )

    # --------------------------------------------------------
    # FWD
    # --------------------------------------------------------

    padrao = re.search(
        r"FWD\s*:\s*(.*?)(?:\.\.\.|$)",
        bloco,
        re.IGNORECASE
    )

    if padrao:

        texto = padrao.group(1)

        texto = re.sub(
            r"\s+\d+\.\s*",
            ", ",
            texto
        )

        partes = re.split(
            r",|\s+e\s+",
            texto
        )

        for parte in partes:

            adicionar_jogador(
                jogadores,
                parte
            )

    return jogadores


# ============================================================
# EXTRAIR ESCALAÇÃO POR LISTA
# ============================================================

def extrair_lista_escalação(texto):

    jogadores = []

    padroes = [

        r"(?:starting lineup|starting line-up|starting XI)\s*:\s*(.*?)(?:\.\.\.|$)",

        r"(?:Marseille|Strasbourg)\s+starting lineup\s*:\s*(.*?)(?:\.\.\.|$)"
    ]

    for padrao in padroes:

        encontrados = re.findall(
            padrao,
            texto,
            re.IGNORECASE
        )

        for bloco in encontrados:

            partes = re.split(
                r",|\s+e\s+",
                bloco
            )

            for parte in partes:

                adicionar_jogador(
                    jogadores,
                    parte
                )

    return jogadores


# ============================================================
# EXTRAIR ESCALAÇÃO EM PORTUGUÊS
# ============================================================

def extrair_portugues(
    texto,
    time
):

    jogadores = []

    if time.lower() == "marseille":

        padrao = re.search(
            r"(?:Olympique de Marseille|Marseille)\s*:\s*(.*?)(?:Técnico:|Strasbourg\s*:)",
            texto,
            re.IGNORECASE
        )

    else:

        padrao = re.search(
            r"Strasbourg\s*:\s*(.*?)(?:Técnico:|$)",
            texto,
            re.IGNORECASE
        )

    if not padrao:

        return jogadores

    bloco = padrao.group(1)

    # --------------------------------------------------------
    # Separar primeiro por ;
    # --------------------------------------------------------

    blocos = bloco.split(";")

    for parte_bloco in blocos:

        # Separar vírgulas
        partes = re.split(
            r",",
            parte_bloco
        )

        for parte in partes:

            # Algumas fontes usam " e "
            subpartes = re.split(
                r"\s+e\s+",
                parte
            )

            for subparte in subpartes:

                adicionar_jogador(
                    jogadores,
                    subparte
                )

    return jogadores


# ============================================================
# EXTRAIR FORMATO COM HÍFENS
# ============================================================

def extrair_formato_hifen(
    texto
):

    jogadores = []

    # Exemplo:
    #
    # Rulli - Emerson, Medina, Balerdi, Weah -
    # Højbjerg, Nadi - Igor Paixão, Gouiri...
    #

    padrao = re.search(
        r"\(probable line-up\)\s*:\s*(.*?)(?:\.\.\.|$)",
        texto,
        re.IGNORECASE
    )

    if not padrao:

        return jogadores

    bloco = padrao.group(1)

    partes = re.split(
        r"\s+-\s+|,",
        bloco
    )

    for parte in partes:

        adicionar_jogador(
            jogadores,
            parte
        )

    return jogadores


# ============================================================
# REMOVER DUPLICIDADES
# ============================================================

def remover_duplicados(jogadores):

    resultado = []

    vistos = set()

    for jogador in jogadores:

        chave = jogador.lower()

        if chave in vistos:
            continue

        vistos.add(chave)

        resultado.append(jogador)

    return resultado


# ============================================================
# EXTRAIR JOGADORES
# ============================================================

def extrair_jogadores(resultado):

    titulo = resultado.get(
        "title",
        ""
    )

    conteudo = resultado.get(
        "content",
        ""
    )

    texto = conteudo or ""

    # Normalizar espaços
    texto = texto.replace(
        "\n",
        " "
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    jogadores = []

    # ========================================================
    # FONTE COM GK / DEF / MID / FWD
    # ========================================================

    bloco_marseille = extrair_bloco_time(
        texto,
        "Marseille"
    )

    if bloco_marseille:

        jogadores.extend(
            extrair_posicoes(
                bloco_marseille
            )
        )

    bloco_strasbourg = extrair_bloco_time(
        texto,
        "Strasbourg"
    )

    if bloco_strasbourg:

        jogadores.extend(
            extrair_posicoes(
                bloco_strasbourg
            )
        )

    # ========================================================
    # FONTE EM PORTUGUÊS
    # ========================================================

    jogadores.extend(
        extrair_portugues(
            texto,
            "Marseille"
        )
    )

    jogadores.extend(
        extrair_portugues(
            texto,
            "Strasbourg"
        )
    )

    # ========================================================
    # STARTING LINEUP
    # ========================================================

    jogadores.extend(
        extrair_lista_escalação(
            texto
        )
    )

    # ========================================================
    # FORMATO RATINGBET
    # ========================================================

    jogadores.extend(
        extrair_formato_hifen(
            texto
        )
    )

    # ========================================================
    # REMOVER DUPLICIDADES
    # ========================================================

    jogadores = remover_duplicados(
        jogadores
    )

    # ========================================================
    # RETORNO
    # ========================================================

    return {
        "titulo": titulo,
        "jogadores": jogadores,
        "total_jogadores": len(jogadores)
    }
