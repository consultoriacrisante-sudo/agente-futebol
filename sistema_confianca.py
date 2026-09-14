"""
sistema_confianca.py

Agrega jogadores vindos de VÁRIAS fontes (já usando normalizar_nomes.py
para não contar "Romero" e "Lucas Romero" como jogadores diferentes) e
classifica a confiança de cada jogador:

  🟢 ALTA   — aparece em uma fonte CONFIRMADA, ou em 3+ fontes
  🟡 MÉDIA  — aparece em exatamente 2 fontes (nenhuma confirmada)
  🔴 BAIXA  — aparece em apenas 1 fonte

Regra herdada da documentação original do projeto:
  fonte confirmada > quantidade de fontes concordando.

Depende apenas de normalizar_nomes.py (mesma pasta).
"""

from normalizar_nomes import agrupar_jogadores


# ============================================================
# CLASSIFICAR UM JOGADOR
# ============================================================

def classificar_confianca(total_fontes: int, tem_fonte_confirmada: bool) -> tuple[str, str]:
    """Retorna (nivel, emoji) para um jogador."""

    if tem_fonte_confirmada:
        return "alta", "🟢"

    if total_fontes >= 3:
        return "alta", "🟢"

    if total_fontes == 2:
        return "media", "🟡"

    return "baixa", "🔴"


# ============================================================
# CALCULAR CONFIANÇA DE UM TIME
# ============================================================

def calcular_confianca_time(fontes_do_time: list[dict]) -> list[dict]:
    """
    fontes_do_time: lista de dicionários, um por fonte, no formato:
        {
            "url": "...",
            "confirmada": True/False,
            "jogadores": ["Nome 1", "Nome 2", ...]
        }

    Retorna uma lista ordenada de jogadores com sua confiança:
        {
            "jogador": "Lucas Romero",
            "nivel": "alta",
            "emoji": "🟢",
            "total_fontes": 2,
            "fontes": ["url1", "url2"]
        }
    """

    # --------------------------------------------------------
    # JUNTAR TODOS OS NOMES DE TODAS AS FONTES
    # --------------------------------------------------------

    todos_os_nomes = []

    for fonte in fontes_do_time:
        todos_os_nomes.extend(fonte["jogadores"])

    if not todos_os_nomes:
        return []

    # --------------------------------------------------------
    # AGRUPAR VARIAÇÕES (Romero / Lucas Romero -> mesmo jogador)
    # --------------------------------------------------------

    mapa_canonico = agrupar_jogadores(todos_os_nomes)

    # --------------------------------------------------------
    # PARA CADA JOGADOR CANÔNICO, CONTAR FONTES E VERIFICAR CONFIRMAÇÃO
    # --------------------------------------------------------

    dados_por_jogador: dict[str, dict] = {}

    for fonte in fontes_do_time:

        # nomes únicos já convertidos pro canônico, evitando
        # contar a mesma fonte duas vezes pelo mesmo jogador
        canonicos_nesta_fonte = {
            mapa_canonico[nome] for nome in fonte["jogadores"]
        }

        for jogador_canonico in canonicos_nesta_fonte:

            if jogador_canonico not in dados_por_jogador:
                dados_por_jogador[jogador_canonico] = {
                    "total_fontes": 0,
                    "tem_confirmada": False,
                    "fontes": [],
                }

            dados_por_jogador[jogador_canonico]["total_fontes"] += 1
            dados_por_jogador[jogador_canonico]["fontes"].append(fonte["url"])

            if fonte.get("confirmada"):
                dados_por_jogador[jogador_canonico]["tem_confirmada"] = True

    # --------------------------------------------------------
    # MONTAR RESULTADO FINAL
    # --------------------------------------------------------

    resultado = []

    for jogador, dados in dados_por_jogador.items():

        nivel, emoji = classificar_confianca(
            dados["total_fontes"],
            dados["tem_confirmada"],
        )

        resultado.append({
            "jogador": jogador,
            "nivel": nivel,
            "emoji": emoji,
            "total_fontes": dados["total_fontes"],
            "fontes": dados["fontes"],
        })

    # Ordena: confiança alta primeiro, depois por nº de fontes
    ordem_nivel = {"alta": 0, "media": 1, "baixa": 2}

    resultado.sort(
        key=lambda item: (ordem_nivel[item["nivel"]], -item["total_fontes"])
    )

    return resultado


# ============================================================
# EXIBIR RESULTADO (formato legível no terminal)
# ============================================================

def exibir_confianca(nome_time: str, jogadores_com_confianca: list[dict]) -> None:

    print()
    print(f"{nome_time.upper()}")
    print("-" * 60)

    for item in jogadores_com_confianca:
        print(
            f'{item["emoji"]} {item["jogador"]:25} '
            f'({item["total_fontes"]} fonte(s))'
        )


# ============================================================
# TESTE COM DADOS REAIS DOCUMENTADOS (Cruzeiro x Atlético-MG)
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("TESTE — CRUZEIRO (dados reais documentados do projeto)")
    print("=" * 60)

    # Duas fontes reais do documento MEMORIA_AGENTE_FUTEBOL.md,
    # com a divergência real: "Romero" vs "Lucas Romero"

    fontes_cruzeiro = [
        {
            "url": "fonte-a.com/cruzeiro-escalacao",
            "confirmada": False,
            "jogadores": [
                "Otávio", "Fagner", "Fabrício Bruno", "Jonathan Jesus",
                "Rojas", "Gerson", "Romero", "Matheus Pereira",
                "Arroyo", "Kaio Jorge", "Wesley",
            ],
        },
        {
            "url": "fonte-b.com/cruzeiro-escalacao",
            "confirmada": False,
            "jogadores": [
                "Otávio", "Fagner", "Fabrício Bruno", "Jonathan Jesus",
                "Rojas", "Lucas Romero", "Gerson", "Arroyo",
                "Matheus Pereira", "Wesley", "Kaio Jorge",
            ],
        },
    ]

    resultado_cruzeiro = calcular_confianca_time(fontes_cruzeiro)

    exibir_confianca("Cruzeiro", resultado_cruzeiro)

    print()
    print(
        "Repare: 'Romero' e 'Lucas Romero' viraram UM jogador só, "
        "com 2 fontes — sem a normalização, apareceriam como dois "
        "jogadores com 1 fonte cada (🔴 baixa em vez de 🟡 média)."
    )