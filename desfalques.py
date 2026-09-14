from buscar_desfalques import (
    buscar_desfalques,
    formatar_desfalques
)


# ============================================================
# ESTRUTURAR DESFALQUES
# ============================================================

def estruturar_desfalques(fixture_id):

    # ========================================================
    # BUSCAR DADOS NA API
    # ========================================================

    dados = buscar_desfalques(fixture_id)

    # ========================================================
    # VERIFICAR SE EXISTEM DADOS
    # ========================================================

    if not dados:

        return {
            "total": 0,
            "desfalques": []
        }

    # ========================================================
    # FORMATAR DADOS
    # ========================================================

    desfalques = formatar_desfalques(dados)

    # ========================================================
    # RETORNAR ESTRUTURA
    # ========================================================

    return {
        "total": len(desfalques),
        "desfalques": desfalques
    }

