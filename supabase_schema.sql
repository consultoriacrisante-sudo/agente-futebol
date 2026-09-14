create table if not exists public.telegram_users (
  chat_id bigint primary key,
  username text not null default '',
  nome text not null default '',
  ativo boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.app_state (
  chave text primary key,
  valor jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

-- O backend usa SUPABASE_KEY como segredo de servidor.
-- Não exponha essa chave em front-end ou repositório.
