import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("DATA_DIR") or BASE_DIR)
DATA_DIR.mkdir(parents=True, exist_ok=True)

SUPABASE_URL = (os.getenv("SUPABASE_URL") or "").rstrip("/")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or ""

USUARIOS_FILE = DATA_DIR / "usuarios.json"
ESTADO_FILE = DATA_DIR / "estado_bot.json"


def usando_supabase():
    return bool(SUPABASE_URL and SUPABASE_KEY)


def _headers(prefer=None):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }
    if prefer:
        headers["Prefer"] = prefer
    return headers


def _supabase_request(method, path, **kwargs):
    url = f"{SUPABASE_URL}/rest/v1/{path.lstrip('/')}"
    response = requests.request(method, url, headers=_headers(kwargs.pop("prefer", None)), timeout=20, **kwargs)
    response.raise_for_status()
    if not response.content:
        return None
    return response.json()


def listar_usuarios_telegram():
    if usando_supabase():
        try:
            return _supabase_request(
                "GET",
                "telegram_users?select=chat_id,username,nome,ativo&ativo=eq.true&order=created_at.asc",
            ) or []
        except requests.RequestException as erro:
            print(f"Erro Supabase ao listar usuários: {erro}")
            return []

    if not USUARIOS_FILE.exists():
        return []
    try:
        dados = json.loads(USUARIOS_FILE.read_text(encoding="utf-8"))
        return dados if isinstance(dados, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def salvar_usuario_telegram(chat):
    chat_id = int(chat["id"])
    username = chat.get("username", "") or ""
    nome = chat.get("first_name", "") or ""

    if usando_supabase():
        payload = {"chat_id": chat_id, "username": username, "nome": nome, "ativo": True}
        try:
            _supabase_request(
                "POST",
                "telegram_users?on_conflict=chat_id",
                json=payload,
                prefer="resolution=merge-duplicates,return=representation",
            )
            return True
        except requests.RequestException as erro:
            print(f"Erro Supabase ao cadastrar usuário: {erro}")
            return False

    usuarios = listar_usuarios_telegram()
    encontrou = False
    for usuario in usuarios:
        if int(usuario.get("chat_id", 0)) == chat_id:
            usuario.update({"username": username, "nome": nome, "ativo": True})
            encontrou = True
            break
    if not encontrou:
        usuarios.append({"chat_id": chat_id, "username": username, "nome": nome, "ativo": True})
    USUARIOS_FILE.write_text(json.dumps(usuarios, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


def desativar_usuario_telegram(chat_id):
    chat_id = int(chat_id)
    if usando_supabase():
        try:
            _supabase_request("PATCH", f"telegram_users?chat_id=eq.{chat_id}", json={"ativo": False})
            return True
        except requests.RequestException as erro:
            print(f"Erro Supabase ao desativar usuário: {erro}")
            return False

    usuarios = listar_usuarios_telegram()
    for usuario in usuarios:
        if int(usuario.get("chat_id", 0)) == chat_id:
            usuario["ativo"] = False
    USUARIOS_FILE.write_text(json.dumps(usuarios, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


def carregar_estado():
    padrao = {"ultimo_update_id": None, "ultimo_envio_diario": None}
    if usando_supabase():
        try:
            linhas = _supabase_request("GET", "app_state?chave=eq.telegram&select=valor&limit=1") or []
            if linhas and isinstance(linhas[0].get("valor"), dict):
                return {**padrao, **linhas[0]["valor"]}
            return padrao
        except requests.RequestException as erro:
            print(f"Erro Supabase ao carregar estado: {erro}")
            return padrao

    if not ESTADO_FILE.exists():
        return padrao
    try:
        dados = json.loads(ESTADO_FILE.read_text(encoding="utf-8"))
        return {**padrao, **dados} if isinstance(dados, dict) else padrao
    except (OSError, json.JSONDecodeError):
        return padrao


def salvar_estado(**campos):
    estado = carregar_estado()
    for chave, valor in campos.items():
        if valor is not None:
            estado[chave] = valor

    if usando_supabase():
        payload = {"chave": "telegram", "valor": estado}
        try:
            _supabase_request(
                "POST",
                "app_state?on_conflict=chave",
                json=payload,
                prefer="resolution=merge-duplicates,return=minimal",
            )
            return True
        except requests.RequestException as erro:
            print(f"Erro Supabase ao salvar estado: {erro}")
            return False

    ESTADO_FILE.write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")
    return True
