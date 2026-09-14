# Checklist rápido para colocar o Agente Futebol no ar

## 1. GitHub
- Criar um repositório novo (público ou privado).
- Subir todos os arquivos deste ZIP, exceto `.env`.
- Conferir se o workflow `CI` fica verde em **Actions**.

## 2. Supabase
- Criar um projeto gratuito.
- Abrir **SQL Editor** e executar `supabase_schema.sql`.
- Guardar `SUPABASE_URL` e uma chave de servidor adequada para o backend.

## 3. Vercel
- Criar conta e importar o repositório GitHub.
- Adicionar todas as variáveis necessárias do `.env.example` em **Environment Variables**.
- Fazer deploy.
- Copiar a URL final e salvar em `APP_BASE_URL`.

## 4. Telegram
- Criar `TELEGRAM_WEBHOOK_SECRET` (texto aleatório forte).
- Definir `TELEGRAM_USE_WEBHOOK=true` na Vercel.
- Localmente, preencher `APP_BASE_URL`, `TELEGRAM_BOT_TOKEN` e `TELEGRAM_WEBHOOK_SECRET` no `.env`.
- Rodar `python scripts/configurar_telegram_webhook.py` uma única vez.
- Testar no Telegram: `/start` e depois `/jogos`.

## 5. WhatsApp Business Cloud API
Você NÃO precisa enviar seus segredos para outra pessoa. Configure diretamente no painel da Meta/Vercel:

- `WHATSAPP_ACCESS_TOKEN`
- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_VERIFY_TOKEN` (você escolhe o valor)
- `META_APP_SECRET`
- `WHATSAPP_API_VERSION`

Callback do webhook:

`https://SEU-PROJETO.vercel.app/webhook/whatsapp`

Depois assine o evento de mensagens no painel da Meta e teste mandando `jogos` para o número Business.

## 6. Cron diário
- Criar um `CRON_SECRET` forte na Vercel.
- O `vercel.json` já agenda um envio diário por volta das 08:00 de Brasília (11:00 UTC).
- No plano Hobby, a Vercel pode executar dentro da hora configurada, não necessariamente no minuto exato.

## 7. WhatsApp Channels
- Criar o Channel pelo app WhatsApp Business, se quiser o canal de broadcast.
- Este projeto NÃO automatiza postagem em WhatsApp Channels porque Channels e Cloud API de mensagens 1:1 são produtos diferentes e não foi assumida uma API pública de publicação em Channels.
