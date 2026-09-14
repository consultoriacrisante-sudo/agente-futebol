import os
import requests
from dotenv import load_dotenv

from storage import (
    carregar_estado,
    desativar_usuario_telegram,
    listar_usuarios_telegram,
    salvar_estado,
    salvar_usuario_telegram,
)

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def carregar_usuarios():
    return listar_usuarios_telegram()


def cadastrar_usuario(chat):
    return salvar_usuario_telegram(chat)


def dividir_mensagem(texto, limite=3900):
    if len(texto) <= limite:
        return [texto]
    blocos, atual = [], ""
    for paragrafo in texto.split("\n\n"):
        candidato = paragrafo if not atual else atual + "\n\n" + paragrafo
        if len(candidato) <= limite:
            atual = candidato
            continue
        if atual:
            blocos.append(atual)
        if len(paragrafo) <= limite:
            atual = paragrafo
        else:
            linhas = paragrafo.splitlines()
            atual = ""
            for linha in linhas:
                candidato = linha if not atual else atual + "\n" + linha
                if len(candidato) > limite and atual:
                    blocos.append(atual)
                    atual = linha
                else:
                    atual = candidato
    if atual:
        blocos.append(atual)
    return blocos


def enviar_mensagem(chat_id, texto):
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN não configurado.")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    ok = True
    for parte in dividir_mensagem(texto):
        payload = {"chat_id": chat_id, "text": parte, "disable_web_page_preview": True}
        try:
            resposta = requests.post(url, json=payload, timeout=20)
            resposta.raise_for_status()
        except requests.RequestException as erro:
            print(f"Erro ao enviar mensagem Telegram: {erro}")
            ok = False
            break
    return ok


def processar_update(update):
    mensagem = update.get("message") or update.get("edited_message")
    if not mensagem:
        return
    texto = (mensagem.get("text") or "").strip()
    comando = texto.split()[0].lower() if texto else ""
    chat = mensagem.get("chat", {})
    chat_id = chat.get("id")
    if not chat_id:
        return

    if comando == "/start":
        cadastrar_usuario(chat)
        enviar_mensagem(
            chat_id,
            "⚽ Bem-vindo ao Agente Futebol!\n\n"
            "Você está cadastrado para receber o boletim diário.\n"
            "Use /jogos para consultar agora ou /stop para sair.",
        )
        return

    if comando == "/stop":
        desativar_usuario_telegram(chat_id)
        enviar_mensagem(chat_id, "✅ Envio diário desativado. Use /start para voltar.")
        return

    if comando in {"/jogos", "/hoje"}:
        from buscar_jogos import buscar_jogos, filtrar_jogos
        from boletim import montar_boletim
        jogos = filtrar_jogos(buscar_jogos())
        enviar_mensagem(chat_id, montar_boletim(jogos, incluir_transmissao=True))
        return

    if comando == "/ajuda":
        enviar_mensagem(chat_id, "Comandos: /start, /jogos, /hoje, /stop")


def buscar_updates(ultimo_update_id=None):
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN não configurado.")
        return []
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    params = {"timeout": 30}
    if ultimo_update_id is not None:
        params["offset"] = ultimo_update_id + 1
    try:
        resposta = requests.get(url, params=params, timeout=35)
        resposta.raise_for_status()
        return resposta.json().get("result", [])
    except requests.RequestException as erro:
        print(f"Erro ao buscar updates: {erro}")
        return []


__all__ = [
    "buscar_updates", "carregar_estado", "salvar_estado", "processar_update",
    "carregar_usuarios", "enviar_mensagem", "dividir_mensagem"
]
