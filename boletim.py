from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from zoneinfo import ZoneInfo

from formatar_jogos import formatar_jogo
from pesquisar_transmissoes import pesquisar_transmissao

TIMEZONE_BRASILIA = ZoneInfo("America/Sao_Paulo")


def enriquecer_jogos(jogos, incluir_transmissao=True, max_workers=3):
    dados = [formatar_jogo(bruto) for bruto in sorted(jogos, key=lambda item: item["fixture"]["date"])]
    if not incluir_transmissao or not dados:
        for jogo in dados:
            jogo["transmissao"] = None
        return dados

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futuros = {executor.submit(pesquisar_transmissao, jogo): idx for idx, jogo in enumerate(dados)}
        for futuro in as_completed(futuros):
            idx = futuros[futuro]
            try:
                dados[idx]["transmissao"] = futuro.result()
            except Exception as erro:
                print(f"Erro ao enriquecer transmissão: {erro}")
                dados[idx]["transmissao"] = {
                    "resumo": {
                        "confirmada": False,
                        "a_confirmar": False,
                        "texto": "Consulte a programação oficial",
                    }
                }
    return dados


def montar_boletim(jogos, incluir_transmissao=True):
    hoje = datetime.now(TIMEZONE_BRASILIA).strftime("%d/%m/%Y")
    if not jogos:
        return f"⚽ JOGOS DE HOJE\n📅 {hoje}\n\nNenhum jogo monitorado encontrado para hoje."

    dados = enriquecer_jogos(jogos, incluir_transmissao=incluir_transmissao)
    linhas = ["⚽ JOGOS DE HOJE", f"📅 {hoje}", ""]
    campeonato_anterior = None
    primeiro_jogo_campeonato = True

    for jogo in dados:
        mudou_campeonato = jogo["campeonato"] != campeonato_anterior
        if mudou_campeonato:
            if campeonato_anterior is not None:
                linhas.append("")
            linhas.append(f"🏆 {jogo['campeonato']}")
            campeonato_anterior = jogo["campeonato"]
            primeiro_jogo_campeonato = True
        elif not primeiro_jogo_campeonato:
            # Respiro visual entre partidas da mesma competição.
            linhas.append("")

        linhas.append(f"⚽ {jogo['time_casa']} x {jogo['time_fora']}")
        linhas.append(f"🕐 {jogo['horario']}")

        pesquisa = jogo.get("transmissao") or {}
        resumo = pesquisa.get("resumo", {})
        texto = resumo.get("texto") or "Consulte a programação oficial"

        if resumo.get("confirmada"):
            linhas.append(f"📺 {texto}")
            if resumo.get("gratis") is True:
                linhas.append("🆓 Opção gratuita indicada pela fonte")
        elif resumo.get("a_confirmar"):
            linhas.append(f"📺 {texto} (a confirmar)")
        else:
            linhas.append("📺 Consulte a programação oficial")

        primeiro_jogo_campeonato = False

    linhas.extend(["", "🤖 Agente Futebol"])
    return "\n".join(linhas)
