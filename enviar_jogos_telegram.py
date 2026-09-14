from datetime import datetime
from zoneinfo import ZoneInfo

from buscar_jogos import buscar_jogos, filtrar_jogos
from boletim import montar_boletim
from bot_telegram import carregar_usuarios, enviar_mensagem
from storage import carregar_estado, salvar_estado

TIMEZONE_BRASILIA = ZoneInfo("America/Sao_Paulo")


def formatar_jogos(jogos):
    return montar_boletim(jogos, incluir_transmissao=True)


def enviar_jogos_para_usuarios(forcar=False):
    print("\nBUSCANDO JOGOS DO DIA")
    print("=" * 60)
    hoje_iso = datetime.now(TIMEZONE_BRASILIA).strftime("%Y-%m-%d")
    estado = carregar_estado()
    if not forcar and estado.get("ultimo_envio_diario") == hoje_iso:
        print("Boletim de hoje já foi enviado. Envio duplicado evitado.")
        return True

    jogos = filtrar_jogos(buscar_jogos())
    print(f"Jogos encontrados: {len(jogos)}")
    usuarios = [u for u in carregar_usuarios() if u.get("ativo", True) and u.get("chat_id")]
    print(f"Usuários ativos: {len(usuarios)}")
    if not usuarios:
        return False

    mensagem = formatar_jogos(jogos)
    todos_ok = True
    for usuario in usuarios:
        print(f"Enviando para: {usuario.get('nome', 'Usuário')}")
        todos_ok = enviar_mensagem(usuario["chat_id"], mensagem) and todos_ok

    if todos_ok:
        salvar_estado(ultimo_envio_diario=hoje_iso)
    return todos_ok


if __name__ == "__main__":
    enviar_jogos_para_usuarios()
