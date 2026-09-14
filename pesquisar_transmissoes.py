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

# Para "onde assistir no Brasil", priorizamos fontes brasileiras/rights-holder.
FONTES_TRANSMISSAO = [
    ("ge", "ge.globo.com"),
    ("ESPN Brasil", "espn.com.br"),
    ("UOL", "uol.com.br"),
    ("Lance!", "lance.com.br"),
    ("CNN Brasil", "cnnbrasil.com.br"),
    ("Band", "band.uol.com.br"),
    ("SBT Sports", "sbt.com.br"),
]

# Só exibimos nomes encontrados literalmente nas evidências retornadas.
CANAIS = [
    ("Premiere", [r"\bpremiere\b"]),
    ("SporTV", [r"\bsportv\b"]),
    ("Globo", [r"\bglobo\b", r"\btv globo\b"]),
    ("ESPN", [r"\bespn\b"]),
    ("Disney+", [r"\bdisney\+", r"\bdisney plus\b"]),
    ("CazéTV", [r"\bcaz[eé]tv\b"]),
    ("YouTube", [r"\byoutube\b"]),
    ("Prime Video", [r"\bprime video\b", r"\bamazon prime\b"]),
    ("Record", [r"\brecord\b", r"\brecord tv\b"]),
    ("Record News", [r"\brecord news\b"]),
    ("Band", [r"\bband\b", r"\bbandplay\b"]),
    ("SBT", [r"\bsbt\b"]),
    ("Paramount+", [r"\bparamount\+", r"\bparamount plus\b"]),
    ("TNT Sports", [r"\btnt sports\b", r"\btnt\b"]),
    ("Max", [r"\bhbo max\b", r"\bmax\b"]),
    ("DAZN", [r"\bdazn\b"]),
    ("GOAT", [r"\bcanal goat\b", r"\bgoat\b"]),
]

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
    return f'{jogo.get("fixture_id")}:{jogo.get("data")}'


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
        'onde assistir Brasil transmissão TV streaming'
    )


def pesquisar_web(termo):
    if not TAVILY_API_KEY:
        return []
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": termo,
        "search_depth": "advanced",
        "topic": "general",
        "max_results": 8,
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

    # Páginas genéricas de agenda costumam misturar várias partidas e geram falsos positivos.
    if any(termo in titulo for termo in ("agenda de futebol", "calendario", "resultados de hoje")):
        return False

    # Exige referência aos dois times.
    if casa not in texto or fora not in texto:
        return False

    # E exige contexto editorial de transmissão/partida ao vivo.
    return any(termo in texto for termo in (
        "onde assistir", "transmissao", "ao vivo", "watch", "tv", "streaming"
    ))


def _extrair_canais(texto):
    canais = []
    texto_lower = (texto or "").lower()
    for nome, padroes in CANAIS:
        if any(re.search(padrao, texto_lower, flags=re.IGNORECASE) for padrao in padroes):
            if nome not in canais:
                canais.append(nome)
    # Record News antes de Record evita duplicação visual pouco útil.
    if "Record News" in canais and "Record" in canais:
        canais.remove("Record")
    return canais


def _tem_gratis_explicito(texto):
    return any(re.search(padrao, texto or "", flags=re.IGNORECASE) for padrao in TERMOS_GRATIS)


def _consolidar(resultados, jogo):
    evidencias = []
    canais = []
    gratis = False

    ordenados = sorted(resultados, key=lambda r: float(r.get("score", 0) or 0), reverse=True)
    for resultado in ordenados:
        fonte = _fonte_por_url(resultado.get("url", ""))
        if not fonte or not _resultado_relevante(resultado, jogo):
            continue
        texto = re.sub(r"\s+", " ", " ".join([resultado.get("title", ""), resultado.get("content", "")])).strip()
        encontrados = _extrair_canais(texto)
        if not encontrados:
            continue
        for canal in encontrados:
            if canal not in canais:
                canais.append(canal)
        gratis = gratis or _tem_gratis_explicito(texto)
        evidencias.append({
            "fonte": fonte,
            "url": resultado.get("url", ""),
            "score": round(float(resultado.get("score", 0) or 0), 4),
            "canais": encontrados,
        })
        if len(evidencias) >= 2:
            break

    confirmada = bool(canais and evidencias)
    return {
        "confirmada": confirmada,
        "canais": canais if confirmada else [],
        "gratis": True if confirmada and gratis else False,
        "fontes": evidencias,
        "texto": " / ".join(canais) if confirmada else "Transmissão não confirmada",
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
