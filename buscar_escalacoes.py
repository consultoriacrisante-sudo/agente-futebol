import requests
import os

from dotenv import load_dotenv


# ============================================================
# CONFIGURAÇÃO
# ============================================================

load_dotenv()

TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY"
)

URL = "https://api.tavily.com/search"


# ============================================================
# EXECUTAR UMA PESQUISA
# ============================================================

def executar_busca(
    consulta,
    max_results=5
):

    payload = {

        "api_key":
            TAVILY_API_KEY,

        "query":
            consulta,

        "search_depth":
            "advanced",

        "topic":
            "news",

        "max_results":
            max_results,

        "include_answer":
            False
    }

    try:

        response = requests.post(

            URL,

            json=payload,

            timeout=30
        )

    except requests.RequestException as erro:

        print()
        print(
            "Erro de conexão com Tavily:"
        )

        print(erro)

        return []


    # ========================================================
    # VALIDAR RESPOSTA
    # ========================================================

    if response.status_code != 200:

        print()
        print(
            "Erro ao consultar Tavily."
        )

        print(
            f"Status HTTP: "
            f"{response.status_code}"
        )

        return []


    try:

        data = response.json()

    except ValueError:

        print()
        print(
            "Resposta inválida da API."
        )

        return []


    return data.get(
        "results",
        []
    )


# ============================================================
# REMOVER RESULTADOS DUPLICADOS
# ============================================================

def remover_duplicados(
    resultados
):

    encontrados = set()

    unicos = []

    for resultado in resultados:

        url = resultado.get(
            "url",
            ""
        )

        if not url:

            continue

        if url in encontrados:

            continue

        encontrados.add(
            url
        )

        unicos.append(
            resultado
        )

    return unicos


# ============================================================
# CALCULAR PONTUAÇÃO DA FONTE
# ============================================================

def pontuar_fonte(
    resultado
):

    url = resultado.get(
        "url",
        ""
    ).lower()

    titulo = resultado.get(
        "title",
        ""
    ).lower()

    conteudo = resultado.get(
        "content",
        ""
    ).lower()


    score = float(
        resultado.get(
            "score",
            0
        )
    )


    # ========================================================
    # FONTES PRIORITÁRIAS
    # ========================================================

    fontes = {

        "whoscored.com":
            1.00,

        "sofascore.com":
            0.95,

        "365scores.com":
            0.90,

        "fotmob.com":
            0.90,

        "espn.com":
            0.85,

        "lance.com.br":
            0.80,

        "band.com.br":
            0.75,

        "goal.com":
            0.75,

        "correiobraziliense.com.br":
            0.70,

        "netflu.com.br":
            0.60,

        "netvasco.com.br":
            0.60
    }


    multiplicador = 1.0


    for fonte, valor in fontes.items():

        if fonte in url:

            multiplicador = valor

            break


    score *= multiplicador


    # ========================================================
    # PALAVRAS QUE INDICAM ESCALAÇÃO
    # ========================================================

    palavras_positivas = [

        "lineup",

        "starting xi",

        "starting eleven",

        "starting lineup",

        "probable lineup",

        "predicted lineup",

        "expected lineup",

        "possible lineup",

        "escalação provável",

        "escalações prováveis",

        "escalação",

        "titulares"
    ]


    texto = (
        titulo + " " + conteudo
    )


    for palavra in palavras_positivas:

        if palavra in texto:

            score += 0.05


    # ========================================================
    # NOMES DE POSIÇÕES
    # ========================================================

    posicoes = [

        "goalkeeper",

        "defenders",

        "defender",

        "midfielders",

        "midfielder",

        "forwards",

        "forward",

        "goleiro",

        "defesa",

        "meio-campo",

        "atacante"
    ]


    quantidade_posicoes = 0


    for posicao in posicoes:

        if posicao in texto:

            quantidade_posicoes += 1


    score += (
        quantidade_posicoes * 0.03
    )


    # ========================================================
    # RETORNAR RESULTADO
    # ========================================================

    resultado["_score_agente"] = round(
        score,
        6
    )

    return resultado


# ============================================================
# BUSCAR PROVÁVEIS ESCALAÇÕES
# ============================================================

def buscar_escalacoes(
    time_casa,
    time_fora,
    campeonato,
    data
):

    print()
    print(
        "BUSCANDO ESCALAÇÕES"
    )
    print(
        "=" * 60
    )


    # ========================================================
    # DATA
    # ========================================================

    data_curta = data

    if "T" in data:

        data_curta = data.split(
            "T"
        )[0]


    # ========================================================
    # CONSULTAS
    # ========================================================

    consultas = [

        (
            f'"{time_casa}" '
            f'"{time_fora}" '
            f'lineup '
            f'{data_curta}'
        ),

        (
            f'"{time_casa}" '
            f'"{time_fora}" '
            f'"starting XI" '
            f'{data_curta}'
        ),

        (
            f'"{time_casa}" '
            f'"{time_fora}" '
            f'"probable lineup" '
            f'{data_curta}'
        ),

        (
            f'"{time_casa}" '
            f'"{time_fora}" '
            f'"predicted lineup" '
            f'{data_curta}'
        ),

        (
            f'"{time_casa}" '
            f'"{time_fora}" '
            f'"team news" '
            f'{data_curta}'
        ),

        (
            f'"{time_casa}" '
            f'"{time_fora}" '
            f'escalação '
            f'{data_curta}'
        ),

        (
            f'"{time_casa}" '
            f'"{time_fora}" '
            f'titulares '
            f'{data_curta}'
        )
    ]


    resultados = []


    # ========================================================
    # EXECUTAR CONSULTAS
    # ========================================================

    for i, consulta in enumerate(
        consultas,
        start=1
    ):

        print()
        print(
            f"Pesquisa {i}/"
            f"{len(consultas)}"
        )

        print(
            consulta
        )


        encontrados = executar_busca(
            consulta,
            max_results=5
        )


        print(
            f"Resultados encontrados: "
            f"{len(encontrados)}"
        )


        resultados.extend(
            encontrados
        )


    # ========================================================
    # REMOVER DUPLICADOS
    # ========================================================

    resultados = remover_duplicados(
        resultados
    )


    # ========================================================
    # PONTUAR
    # ========================================================

    resultados = [

        pontuar_fonte(
            resultado
        )

        for resultado in resultados
    ]


    # ========================================================
    # ORDENAR
    # ========================================================

    resultados.sort(

        key=lambda resultado:
            resultado.get(
                "_score_agente",
                0
            ),

        reverse=True
    )


    # ========================================================
    # LIMITAR RESULTADOS
    # ========================================================

    resultados = resultados[:15]


    # ========================================================
    # EXIBIR RESUMO
    # ========================================================

    print()
    print(
        "=" * 60
    )

    print(
        f"TOTAL DE FONTES ÚNICAS: "
        f"{len(resultados)}"
    )


    for i, resultado in enumerate(
        resultados,
        start=1
    ):

        print()
        print(
            f"{i}. "
            f"{resultado.get('title')}"
        )

        print(
            f"Score agente: "
            f"{resultado.get('_score_agente')}"
        )

        print(
            f"URL: "
            f"{resultado.get('url')}"
        )


    print()
    print(
        "=" * 60
    )


    return resultados
