import urllib.parse


# ============================================================
# CRIAR CONSULTA DE TRANSMISSAO
# ============================================================

def criar_consulta_transmissao(jogo):
    """
    Prepara os dados necessários para pesquisar
    onde um jogo será transmitido no Brasil.
    """

    return {
        "campeonato": jogo["campeonato"],
        "time_casa": jogo["time_casa"],
        "time_fora": jogo["time_fora"],
        "data": jogo["data"],
        "horario": jogo["horario"],
        "fixture_id": jogo["fixture_id"],
        "pais": "Brasil"
    }


# ============================================================
# CRIAR PESQUISA
# ============================================================

def criar_busca_google(consulta):
    """
    Cria uma pesquisa direcionada para encontrar
    informações de transmissão no Brasil.
    """

    pesquisa = (
        f'"{consulta["time_casa"]}" '
        f'"{consulta["time_fora"]}" '
        f'"{consulta["campeonato"]}" '
        f'"{consulta["data"]}" '
        f'"onde assistir" '
        f'"Brasil"'
    )

    return (
        "https://www.google.com/search?q="
        + urllib.parse.quote(pesquisa)
    )


# ============================================================
# FONTES PRIORITARIAS
# ============================================================

def criar_buscas_fontes(consulta):
    """
    Cria pesquisas direcionadas para fontes esportivas
    consideradas prioritárias.
    """

    jogo = (
        f'"{consulta["time_casa"]}" '
        f'"{consulta["time_fora"]}" '
        f'"{consulta["data"]}" '
        f'"onde assistir"'
    )

    fontes = {

        "GE": f'{jogo} site:ge.globo.com',

        "ESPN": f'{jogo} site:espn.com.br',

        "UOL Esporte": f'{jogo} site:uol.com.br/esporte',

        "Lance": f'{jogo} site:lance.com.br',

        "CNN Brasil": f'{jogo} site:cnnbrasil.com.br/esportes',

        "SBT Sports": f'{jogo} site:sbt.com.br',

        "Veja": f'{jogo} site:veja.abril.com.br',

        "Placar": f'{jogo} site:placar.com.br'
    }

    buscas = {}

    for fonte, pesquisa in fontes.items():

        buscas[fonte] = (
            "https://www.google.com/search?q="
            + urllib.parse.quote(pesquisa)
        )

    return buscas


# ============================================================
# EXIBIR CONSULTA
# ============================================================

def exibir_consulta(jogo):

    consulta = criar_consulta_transmissao(jogo)

    busca_google = criar_busca_google(consulta)

    buscas_fontes = criar_buscas_fontes(consulta)

    print()
    print("=" * 60)
    print("PESQUISA DE TRANSMISSÃO")
    print("=" * 60)

    print(f'Competição: {consulta["campeonato"]}')

    print(
        f'Jogo: {consulta["time_casa"]} '
        f'x {consulta["time_fora"]}'
    )

    print(f'Data: {consulta["data"]}')
    print(f'Horário: {consulta["horario"]}')
    print(f'Fixture ID: {consulta["fixture_id"]}')
    print(f'País: {consulta["pais"]}')

    print()
    print("PESQUISA GERAL:")
    print(busca_google)

    print()
    print("PESQUISAS POR FONTE:")
    print("-" * 60)

    for fonte, url in buscas_fontes.items():

        print()
        print(f"{fonte}:")
        print(url)