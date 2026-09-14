"""
enviar_telegram.py

Etapa 1 do agente-futebol: envio de mensagens via Telegram.

Este arquivo é isolado de propósito — não depende de buscar_escalacoes.py
nem de nenhuma outra parte do projeto. A ideia é testar o envio sozinho
antes de conectar com o resto.

Pré-requisitos:
- TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no .env
- pip install python-dotenv requests
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def enviar_mensagem_telegram(texto: str) -> bool:
    """
    Envia uma mensagem de texto para o chat configurado no .env.

    Suporta formatação Markdown (negrito com *texto*, links [texto](url), etc.),
    que será útil quando gerarmos o relatório completo mais pra frente.

    Retorna True se o envio deu certo, False caso contrário.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não encontrados no .env")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,  # queremos preview de link (útil pro link da transmissão)
    }

    try:
        resposta = requests.post(url, json=payload, timeout=10)
        resposta.raise_for_status()
        print("✅ Mensagem enviada com sucesso!")
        return True
    except requests.exceptions.RequestException as erro:
        print(f"❌ Erro ao enviar mensagem: {erro}")
        if hasattr(erro, "response") and erro.response is not None:
            print(f"Detalhes: {erro.response.text}")
        return False


if __name__ == "__main__":
    mensagem_teste = (
        "⚽ *Agente Futebol conectado!*\n\n"
        "Se você está recebendo esta mensagem, a integração com o "
        "Telegram está funcionando corretamente.\n\n"
        "Próximo passo: conectar com a busca de escalações."
    )
    enviar_mensagem_telegram(mensagem_teste)
