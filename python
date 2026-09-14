"""
normalizar_nomes.py

Resolve o problema de fontes diferentes escreverem o mesmo jogador
de formas diferentes:
  - "Romero" vs "Lucas Romero"        (nome incompleto)
  - "Victor Hugo" vs "Vitor Hugo"     (variação de grafia)
  - "Højbjerg" vs "Hojbjerg"          (acentuação)

Sem isso, o sistema de confiança (próxima etapa) conta cada variação
como um jogador diferente e a confiança sai errada.

Este arquivo é isolado — não depende de nenhum outro módulo do projeto.
"""

import re
import unicodedata
from difflib import SequenceMatcher


# ============================================================
# REMOVER ACENTOS
# ============================================================

def remover_acentos(texto: str) -> str:
    """Transforma 'Højbjerg' -> 'Hojbjerg', 'Jörgensen' -> 'Jorgensen'."""
    forma_normalizada = unicodedata.normalize("NFKD", texto)
    return "".join(
        caractere
        for caractere in forma_normalizada
        if not unicodedata.combining(caractere)
    )


# ============================================================
# NORMALIZAR NOME (chave de comparação)
# ============================================================

def normalizar_nome(nome: str) -> str:
    """
    Gera uma versão "chave" do nome, só para comparação interna.
    Não é o nome que deve ser exibido no relatório.
    """
    nome = remover_acentos(nome)
    nome = nome.lower().strip()
    nome = re.sub(r"[^\w\s]", "", nome)   # remove pontuação
    nome = re.sub(r"\s+", " ", nome)      # espaços duplicados
    return nome


# ============================================================
# COMPARAR DOIS NOMES
# ============================================================

def nomes_sao_equivalentes(nome_a: str, nome_b: str, limiar: float = 0.85) -> bool:
    """
    Decide se dois nomes provavelmente são a mesma pessoa.

    Duas estratégias, combinadas:

    1. TOKENS: se todas as palavras do nome mais curto aparecem no
       nome mais longo, é o mesmo jogador com nome incompleto.
       Ex: "Romero" está contido em "Lucas Romero" -> equivalente.

    2. SIMILARIDADE: se os nomes completos são muito parecidos
       (diferença de grafia, ex: "Victor Hugo" vs "Vitor Hugo"),
       usamos a razão de similaridade de string.
    """

    chave_a = normalizar_nome(nome_a)
    chave_b = normalizar_nome(nome_b)

    if not chave_a or not chave_b:
        return False

    if chave_a == chave_b:
        return True

    # --- Estratégia 1: subconjunto de palavras -----------------
    tokens_a = set(chave_a.split())
    tokens_b = set(chave_b.split())

    menor, maior = sorted([tokens_a, tokens_b], key=len)

    if menor and menor.issubset(maior):
        return True

    # --- Estratégia 2: similaridade de grafia -------------------
    razao = SequenceMatcher(None, chave_a, chave_b).ratio()

    return razao >= limiar


# ============================================================
# AGRUPAR VARIAÇÕES DE UM MESMO JOGADOR
# ============================================================

def agrupar_jogadores(lista_de_nomes: list[str]) -> dict[str, str]:
    """
    Recebe uma lista de nomes (possivelmente com variações) e devolve
    um dicionário {nome_original: nome_canonico}.

    O nome canônico escolhido é sempre o mais completo (mais longo)
    dentro do grupo — assim "Romero" vira "Lucas Romero" no resultado
    final, não o contrário.
    """

    grupos: list[list[str]] = []

    for nome in lista_de_nomes:

        encontrou_grupo = False

        for grupo in grupos:

            if nomes_sao_equivalentes(nome, grupo[0]):
                grupo.append(nome)
                encontrou_grupo = True
                break

        if not encontrou_grupo:
            grupos.append([nome])

    mapa_canonico = {}

    for grupo in grupos:
        nome_canonico = max(grupo, key=len)
        for nome in grupo:
            mapa_canonico[nome] = nome_canonico

    return mapa_canonico


# ============================================================
# TESTE COM CASOS REAIS DO PROJETO
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("TESTE — CASOS REAIS DOCUMENTADOS NO PROJETO")
    print("=" * 60)

    casos = [
        ("Romero", "Lucas Romero"),
        ("Victor Hugo", "Vitor Hugo"),
        ("Hojbjerg", "Højbjerg"),
        ("Kaio Jorge", "Wesley"),  # não deve dar match
    ]

    for nome_a, nome_b in casos:
        resultado = nomes_sao_equivalentes(nome_a, nome_b)
        simbolo = "✅ EQUIVALENTE" if resultado else "❌ DIFERENTE"
        print(f"\n'{nome_a}'  vs  '{nome_b}'  ->  {simbolo}")

    print()
    print("=" * 60)
    print("TESTE — AGRUPAMENTO DE LISTA COM VARIAÇÕES")
    print("=" * 60)

    lista_cruzeiro = [
        "Romero", "Lucas Romero", "Gerson", "Kaio Jorge",
    ]

    agrupado = agrupar_jogadores(lista_cruzeiro)

    for original, canonico in agrupado.items():
        print(f"{original!r:20} -> {canonico!r}")
