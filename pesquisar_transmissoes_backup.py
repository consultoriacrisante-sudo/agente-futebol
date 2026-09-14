import requests
from bs4 import BeautifulSoup


# ============================================================
# CONFIGURACAO
# ============================================================

FONTES_PRIORITARIAS = {
    "UOL Esporte": "uol.com.br",
    "GE": "ge.globo.com",
    "ESPN Brasil": "espn.com.br",
    "Lance": "lance.com.br",
    "CNN Brasil": "cnnbrasil.com.br",
    "Gazeta Esportiva": "gazetaesportiva.com",
    "Band": "band.com.br",
    "SBT Sports": "sbt.com.br",
    "Placar": "placar.com.br"
}


# ============================================================
# CRIAR PESQUISA
# ============================================================

def criar_termo_pesquisa(jogo):

    return (
        f'{jogo["time_casa"]} '
        f'{jogo["time_fora"]} '
        f'{jogo["campeonato"]} '
        f'{jogo["data"]} '
        f'onde assistir Brasil'
    )


# ============================================================
# PESQUISAR NA WEB
# ============================================================

def pesquisar_web(termo):

    url = "https://www.google.com/search"

    parametros = {
        "q": termo,
        "hl": "pt-BR",
        "gl": "br"
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/142.0 Safari/537.36"
        )
    }

    try:

        response = requests.get(
            url,
            params=parametros,
            headers=headers,
            timeout=20
        )

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        resultados = []

        for resultado in soup.select("div.MjjYud"):

            titulo = resultado.select_one("h3")

            link = resultado.select_one("a")

            descricao = resultado.select_one(
                ".VwiC3b"
            )

            if not titulo or not link:
                continue

            resultados.append({
                "titulo": titulo.get_text(
                    " ",
                    strip=True
                ),
                "url": link.get("href"),
                "descricao": (
                    descricao.get_text(
                        " ",
                        strip=True
                    )
                    if descricao
                    else ""
                )
            })

        return resultados

    except Exception as erro:

        print(
            f"Erro durante pesquisa: {erro}"
        )

        return []


# ============================================================
# FILTRAR FONTES CONFIAVEIS
# ============================================================

def filtrar_fontes(resultados):

    encontrados = []

    for resultado in resultados:

        url = resultado["url"]

        for fonte, dominio in FONTES_PRIORITARIAS.items():

            if dominio in url:

                encontrados.append({
                    "fonte": fonte,
                    "titulo": resultado["titulo"],
                    "url": url,
                    "descricao": resultado["descricao"]
                })

                break

    return encontrados


# ============================================================
# PESQUISAR TRANSMISSAO
# ============================================================

def pesquisar_transmissao(jogo):

    termo = criar_termo_pesquisa(jogo)

    resultados = pesquisar_web(termo)

    fontes = filtrar_fontes(resultados)

    return {
        "jogo": jogo,
        "termo": termo,
        "resultados": fontes
    }


# ============================================================
# EXIBIR RESULTADO
# ============================================================

def exibir_resultado(resultado):

    jogo = resultado["jogo"]

    print()
    print("=" * 60)
    print("RESULTADO DA PESQUISA")
    print("=" * 60)

    print(
        f'Jogo: {jogo["time_casa"]} '
        f'x {jogo["time_fora"]}'
    )

    print(
        f'Competição: {jogo["campeonato"]}'
    )

    print(
        f'Data: {jogo["data"]}'
    )

    print(
        f'Horário: {jogo["horario"]}'
    )

    print()
    print("FONTES ENCONTRADAS")
    print("-" * 60)

    if not resultado["resultados"]:

        print(
            "Nenhuma fonte prioritária encontrada."
        )

        return

    for item in resultado["resultados"]:

        print()
        print(
            f'Fonte: {item["fonte"]}'
        )

        print(
            f'Título: {item["titulo"]}'
        )

        print(
            f'URL: {item["url"]}'
        )

        print(
            f'Descrição: {item["descricao"]}'
        )
