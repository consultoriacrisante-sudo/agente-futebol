import hashlib
import hmac
import os
import requests
from dotenv import load_dotenv

load_dotenv()
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v25.0")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
META_APP_SECRET = os.getenv("META_APP_SECRET")


def configurado():
    return bool(WHATSAPP_ACCESS_TOKEN and WHATSAPP_PHONE_NUMBER_ID)


def verificar_assinatura(payload_bytes, assinatura):
    if not META_APP_SECRET:
        return True
    if not assinatura or not assinatura.startswith("sha256="):
        return False
    esperado = hmac.new(META_APP_SECRET.encode(), payload_bytes, hashlib.sha256).hexdigest()
    recebido = assinatura.split("=", 1)[1]
    return hmac.compare_digest(esperado, recebido)


def _dividir(texto, limite=3900):
    if len(texto) <= limite:
        return [texto]
    partes, atual = [], ""
    for bloco in texto.split("\n\n"):
        candidato = bloco if not atual else atual + "\n\n" + bloco
        if len(candidato) <= limite:
            atual = candidato
        else:
            if atual:
                partes.append(atual)
            atual = bloco
    if atual:
        partes.append(atual)
    return partes


def enviar_texto(numero, texto):
    if not configurado():
        print("WhatsApp não configurado.")
        return False
    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}", "Content-Type": "application/json"}
    for parte in _dividir(texto):
        payload = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "text",
            "text": {"body": parte, "preview_url": False},
        }
        try:
            resposta = requests.post(url, headers=headers, json=payload, timeout=25)
            resposta.raise_for_status()
        except requests.RequestException as erro:
            print(f"Erro WhatsApp: {erro}")
            if getattr(erro, "response", None) is not None:
                print(erro.response.text)
            return False
    return True


def extrair_mensagens(payload):
    mensagens = []
    try:
        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                for msg in value.get("messages", []):
                    texto = msg.get("text", {}).get("body", "")
                    mensagens.append({"numero": msg.get("from"), "texto": texto, "id": msg.get("id")})
    except (AttributeError, TypeError):
        pass
    return mensagens
