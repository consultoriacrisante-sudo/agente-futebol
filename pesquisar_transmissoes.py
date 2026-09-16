import json
import os
import re
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
DATA_DIR = Path(os.getenv("DATA_DIR") or Path(__file__).resolve().parent)
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = DATA_DIR / "transmissoes_cache.json"
CACHE_HORAS = int(os.getenv("TRANSMISSAO_CACHE_HORAS", "12"))

FONTES_TRANSMISSAO = [
    ("ge", "ge.globo.com"),
    ("ESPN Brasil", "espn.com.br"),
    ("UOL", "uol.com.br"),
    ("Lance!", "lance.com.br"),
    ("CNN Brasil", "cnnbrasil.com.br"),
    ("Band", "band.uol.com.br"),
    ("SBT Sports", "sbt.com.br"),
    ("OneFootball", "onefootball.com.br"),
]

CANAIS = [
    ("Premiere", [r"\bpremiere\b"]),
    ("SporTV", [r"\bsportv\b"]),
    ("ge TV", [r"\bge tv\b", r"\bgetv\b"]),
    ("Globo", [r"\bglobo\b", r"\btv globo\b"]),
    ("ESPN", [r"\bespn\b"]),
    ("Disney+", [r"\bdisney\+", r"\bdisney plus\b"]),
    ("CazéTV", [r"\bcaz[eé]tv\b"]),
    ("YouTube", [r"\byoutube\b"]),
    ("Prime Video", [r"\bprime video\b", r"\bamazon prime\b"]),
    ("Record News", [r"\brecord news\b"]),
    ("Record", [r"\brecord\b", r"\brecord tv\b"]),
    ("Band", [r"\bband\b", r"\bbandplay\b"]),
    ("SBT", [r"\bsbt\b"]),
    ("Paramount+", [r"\bparamount\+", r"\bparamount plus\b"]),
    ("TNT Sports", [r"\btnt sports\b", r"\btnt\b"]),
    ("Max", [r"\bhbo max\b", r"\bmax\b"]),
    ("DAZN", [r"\bdazn\b"]),
    ("GOAT", [r"\bcanal goat\b", r"\bgoat\b"]),
    ("OneFootball", [r"\bonefootball\b"]),
    ("SportyNet", [r"\bsportynet\b"]),
    ("XSports", [r"\bxsports\b"]),
    ("NSports", [r"\bnsports\b"]),
]

# Fallback editorial: detentores/plataformas que costumam dividir os direitos no
# Brasil. Nunca é exibido como transmissão confirmada; serve apenas para orientar
# o usuário quando a busca do jogo específico ainda não encontrou programação.
CANAIS_POR_COMPETICAO = {
    71: ["Premiere", "Globo", "Record"],
    73: ["Globo", "SporTV", "Prime Video"],
    39: ["ESPN", "Disney+"],
    45: ["ESPN", "Disney+"],
    140: ["CazéTV", "ESPN", "Disney+"],
    143: ["ESPN", "Disney+"],
    135: ["ESPN", "Disney+"],
    137: ["ESPN", "Disney+"],
    78: ["OneFootball", "CazéTV", "SporTV"],
    61: ["CazéTV", "XSports"],
    66: ["CazéTV", "XSports"],
    94: ["Disney+", "NSports"],
    96: ["Disney+", "NSports"],
    88: ["Disney+"],
    2: ["TNT Sports", "Max", "SBT"],
    3: ["CazéTV", "Band"],
    848: ["CazéTV", "Band"],
    13: ["Globo/ge TV", "ESPN/Disney+", "Paramount+"],
    11: ["SBT", "ESPN/Disney+", "Paramount+"],
}

TERMOS_GRATIS = [
    r"\bgr[aá]tis\b", r"\bgratuit[oa]\b", r"\bde gra[cç]a\b",
    r"\bsem custo\b", r"\btv aberta\b", r"\bfree\b",
]


def _normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in texto if not unicodedata.combining(c)).lower()


def _dominio(url):
    return urlparse(url).netloc.lower().removeprefix("www.")


def _carregar_cache():
    if not CACHE_FILE.exists():
        return {}
    try:
        dados = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        return dados if isinstance(dados, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _salvar_cache(cache):
    try:
        CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


def _cache_key(jogo):
    return f'{jogo.get("fixture_id")}:{jogo.get("data")}:v3'


def _cache_valido(item):
    try:
        gerado = datetime.fromisoformat(item["gerado_em"])
        if gerado.tzinfo is None:
            gerado = gerado.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) - gerado < timedelta(hours=CACHE_HORAS)
    except (KeyError, TypeError, ValueError):
        return False


def criar_termo_pesquisa(jogo):
    return (
        f'"{jogo["time_casa"]}" "{jogo["time_fora"]}" '
        f'{jogo["campeonato"]} {jogo["data"]} '
        'onde assistir hoje ao vivo Brasil canal transmissão streaming'
    )


def pesquisar_web(termo):
    if not TAVILY_API_KEY:
        return []
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": termo,
        "search_depth": "advanced",
        "topic": "general",
        "max_results": 12,
        "include_answer": False,
        "include_domains": [dominio for _, dominio in FONTES_TRANSMISSAO],
    }
    try:
        response = requests.post("https://api.tavily.com/search", json=payload, timeout=25)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as erro:
        print(f"Erro durante pesquisa Tavily: {erro}")
        return []


def _fonte_por_url(url):
    dominio_url = _dominio(url)
    for fonte, dominio in FONTES_TRANSMISSAO:
        if dominio_url == dominio or dominio_url.endswith("." + dominio):
            return fonte
    return None


def _resultado_relevante(resultado, jogo):
    titulo = _normalizar(resultado.get("title", ""))
    texto = _normalizar(" ".join([resultado.get("title", ""), resultado.get("content", "")]))
    casa = _normalizar(jogo["time_casa"])
    fora = _normalizar(jogo["time_fora"])

    if any(termo in titulo for termo in (
        "agenda de futebol", "calendario", "resultados de hoje", "jogos de hoje",
        "programacao", "programacao esportiva"
    )):
        return False
    if casa not in texto or fora not in texto:
        return False
    return any(termo in texto for termo in (
        "onde assistir", "transmissao", "ao vivo", "watch", "tv", "streaming"
    ))


def _trecho_da_partida(resultado, jogo):
    texto = re.sub(r"\s+", " ", " ".join([
        resultado.get("title", ""), resultado.get("content", "")
    ])).strip()
    normal = _normalizar(texto)
    casa = _normalizar(jogo["time_casa"])
    fora = _normalizar(jogo["time_fora"])
    pos_casa = normal.find(casa)
    pos_fora = normal.find(fora)
    if pos_casa < 0 or pos_fora < 0:
        return ""

    inicio_times = min(pos_casa, pos_fora)
    fim_times = max(pos_casa + len(casa), pos_fora + len(fora))
    if fim_times - inicio_times > 260:
        return ""

    inicio = max(0, inicio_times - 180)
    fim = min(len(texto), fim_times + 380)
    return texto[inicio:fim]


def _extrair_canais(texto):
    canais = []
    texto_lower = (texto or "").lower()
    for nome, padroes in CANAIS:
        if any(re.search(padrao, texto_lower, flags=re.IGNORECASE) for padrao in padroes):
            if nome not in canais:
                canais.append(nome)
    if "Record News" in canais and "Record" in canais:
        canais.remove("Record")
    # ge TV pertence ao Grupo Globo, mas é uma plataforma distinta; evita duplicar
    # Globo apenas quando a evidência menciona explicitamente ge TV sem TV Globo.
    return canais


def _tem_gratis_explicito(texto):
    return any(re.search(padrao, texto or "", flags=re.IGNORECASE) for padrao in TERMOS_GRATIS)


def _canais_provaveis(jogo):
    return CANAIS_POR_COMPETICAO.get(jogo.get("league_id"), [])[:3]


def _consolidar(resultados, jogo):
    evidencias = []
    votos = {}
    gratis_por_canal = set()

    ordenados = sorted(resultados, key=lambda r: float(r.get("score", 0) or 0), reverse=True)
    for resultado in ordenados:
        fonte = _fonte_por_url(resultado.get("url", ""))
        if not fonte or not _resultado_relevante(resultado, jogo):
            continue

        trecho = _trecho_da_partida(resultado, jogo)
        if not trecho:
            continue
        encontrados = _extrair_canais(trecho)
        if not encontrados or len(encontrados) > 4:
            continue

        for canal in encontrados:
            votos.setdefault(canal, set()).add(fonte)
            if _tem_gratis_explicito(trecho):
                gratis_por_canal.add(canal)

        evidencias.append({
            "fonte": fonte,
            "url": resultado.get("url", ""),
            "score": round(float(resultado.get("score", 0) or 0), 4),
            "canais": encontrados,
        })
        if len(evidencias) >= 4:
            break

    canais = []
    if evidencias:
        repetidos = [canal for canal, fontes in votos.items() if len(fontes) >= 2]
        candidatos = repetidos or list(votos.keys())
        canais = candidatos[:3]

    confirmada = bool(canais)
    if confirmada:
        gratis = any(c in gratis_por_canal for c in canais)
        return {
            "confirmada": True,
            "canais": canais,
            "gratis": gratis,
            "fontes": evidencias,
            "texto": " / ".join(canais),
            "a_confirmar": False,
        }

    provaveis = _canais_provaveis(jogo)
    return {
        "confirmada": False,
        "canais": provaveis,
        "gratis": False,
        "fontes": [],
        "texto": " / ".join(provaveis) if provaveis else "Consulte a programação oficial",
        "a_confirmar": bool(provaveis),
    }


def pesquisar_transmissao(jogo, usar_cache=True):
    chave = _cache_key(jogo)
    cache = _carregar_cache() if usar_cache else {}
    item = cache.get(chave)
    if item and _cache_valido(item):
        return item["resultado"]

    termo = criar_termo_pesquisa(jogo)
    resultados = pesquisar_web(termo)
    resumo = _consolidar(resultados, jogo)
    resposta = {"resumo": resumo, "termo": termo}

    if usar_cache:
        cache[chave] = {"gerado_em": datetime.now(timezone.utc).isoformat(), "resultado": resposta}
        _salvar_cache(cache)
    return resposta
