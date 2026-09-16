from datetime import datetime
from zoneinfo import ZoneInfo

from config import CAMPEONATOS


TIMEZONE_BRASILIA = ZoneInfo("America/Sao_Paulo")


def formatar_jogo(jogo):

    league_id = jogo["league"]["id"]

    campeonato = CAMPEONATOS[league_id]

    # --------------------------------------------------------
    # TIMES
    # --------------------------------------------------------

    time_casa = jogo["teams"]["home"]["name"]
    time_fora = jogo["teams"]["away"]["name"]

    # --------------------------------------------------------
    # DATA E HORARIO
    # --------------------------------------------------------

    data_jogo = datetime.fromisoformat(
        jogo["fixture"]["date"].replace("Z", "+00:00")
    )

    data_jogo = data_jogo.astimezone(
        TIMEZONE_BRASILIA
    )

    # --------------------------------------------------------
    # FIXTURE
    # --------------------------------------------------------

    fixture = jogo["fixture"]

    # --------------------------------------------------------
    # ESTADIO
    # --------------------------------------------------------

    venue = fixture.get("venue") or {}

    estadio = venue.get("name")
    cidade = venue.get("city")

    if not estadio:
        estadio = "Não informado"

    if not cidade:
        cidade = "Não informado"

    # --------------------------------------------------------
    # ARBITRO
    # --------------------------------------------------------

    arbitro = fixture.get("referee")

    if not arbitro:
        arbitro = "Não informado"

    # --------------------------------------------------------
    # LIGA
    # --------------------------------------------------------

    rodada = jogo["league"].get("round")

    if not rodada:
        rodada = "Não informado"

    temporada = jogo["league"].get("season")

    if not temporada:
        temporada = "Não informado"

    return {
        "fixture_id": fixture["id"],
        "league_id": league_id,
        "campeonato": campeonato["nome"],
        "pais": campeonato["pais"],
        "regiao": campeonato["regiao"],
        "tipo": campeonato["tipo"],
        "time_casa": time_casa,
        "time_fora": time_fora,
        "data": data_jogo.strftime("%d/%m/%Y"),
        "horario": data_jogo.strftime("%H:%M"),
        "rodada": rodada,
        "temporada": temporada,
        "estadio": estadio,
        "cidade": cidade,
        "arbitro": arbitro,
        "status": fixture["status"]["short"],
        "status_detalhado": fixture["status"]["long"]
    }