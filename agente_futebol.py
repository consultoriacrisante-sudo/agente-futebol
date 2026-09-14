import os
from dotenv import load_dotenv

from bot_telegram import buscar_updates, processar_update
from enviar_jogos_telegram import enviar_jogos_para_usuarios
from storage import carregar_estado, salvar_estado

load_dotenv()


def processar_novos_usuarios():
    if os.getenv("TELEGRAM_USE_WEBHOOK", "false").lower() == "true":
        print("Telegram em modo webhook; getUpdates ignorado.")
        return

    print("\nPROCESSANDO NOVOS USUARIOS")
    print("=" * 60)
    estado = carregar_estado()
    updates = buscar_updates(estado.get("ultimo_update_id"))
    print(f"Novos updates encontrados: {len(updates)}")
    for update in updates:
        processar_update(update)
        update_id = update.get("update_id")
        if update_id is not None:
            salvar_estado(ultimo_update_id=update_id)


def executar_agente(forcar=False):
    print("\nAGENTE FUTEBOL INICIADO")
    print("=" * 60)
    processar_novos_usuarios()
    enviar_jogos_para_usuarios(forcar=forcar)
    print("\n" + "=" * 60)
    print("AGENTE FUTEBOL FINALIZADO")
    print("=" * 60)


if __name__ == "__main__":
    executar_agente()
