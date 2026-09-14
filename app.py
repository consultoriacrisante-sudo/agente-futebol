import os
from flask import Flask, request
from dotenv import load_dotenv

from bot_telegram import processar_update
from buscar_jogos import buscar_jogos, filtrar_jogos
from boletim import montar_boletim
from enviar_jogos_telegram import enviar_jogos_para_usuarios
from whatsapp import WHATSAPP_VERIFY_TOKEN, enviar_texto, extrair_mensagens, verificar_assinatura

load_dotenv()
app = Flask(__name__)
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
CRON_SECRET = os.getenv("CRON_SECRET", "")


def _boletim_hoje():
    return montar_boletim(filtrar_jogos(buscar_jogos()), incluir_transmissao=True)


@app.get("/")
def home():
    return {
        "service": "agente-futebol",
        "status": "ok",
        "commands": ["/start", "/jogos", "/stop"],
    }, 200


@app.get("/health")
def health():
    return {"status": "ok", "service": "agente-futebol"}, 200


@app.post("/webhook/telegram")
def receber_telegram():
    if TELEGRAM_WEBHOOK_SECRET:
        recebido = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if recebido != TELEGRAM_WEBHOOK_SECRET:
            return "forbidden", 403
    payload = request.get_json(silent=True) or {}
    processar_update(payload)
    return "ok", 200


@app.get("/webhook/whatsapp")
def verificar_whatsapp():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and WHATSAPP_VERIFY_TOKEN and token == WHATSAPP_VERIFY_TOKEN:
        return challenge or "", 200
    return "forbidden", 403


@app.post("/webhook/whatsapp")
def receber_whatsapp():
    if not verificar_assinatura(request.get_data(), request.headers.get("X-Hub-Signature-256", "")):
        return "forbidden", 403
    payload = request.get_json(silent=True) or {}
    for mensagem in extrair_mensagens(payload):
        numero = mensagem.get("numero")
        texto = (mensagem.get("texto") or "").strip().lower()
        if not numero:
            continue
        if texto in {"jogos", "jogos de hoje", "hoje", "1", "/jogos"}:
            resposta = _boletim_hoje()
        elif texto in {"start", "oi", "olá", "ola", "menu"}:
            resposta = (
                "⚽ Agente Futebol\n\n"
                "Envie *jogos* para ver os principais jogos de hoje, horários e onde assistir."
            )
        else:
            resposta = "⚽ Digite *jogos* para consultar os jogos de hoje."
        enviar_texto(numero, resposta)
    return "ok", 200


@app.get("/cron/daily")
def cron_daily():
    if CRON_SECRET:
        recebido = request.headers.get("Authorization", "")
        if recebido != f"Bearer {CRON_SECRET}":
            return {"ok": False, "erro": "unauthorized"}, 401
    ok = enviar_jogos_para_usuarios(forcar=False)
    return {"ok": bool(ok)}, 200 if ok else 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
