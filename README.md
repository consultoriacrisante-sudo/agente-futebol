# ⚽ Agente Futebol — MVP final

Agente em Python que consulta os jogos monitorados do dia, identifica **onde assistir no Brasil** sem despejar snippets de busca no usuário e distribui o boletim por Telegram. Também possui webhook para WhatsApp Cloud API em mensagens 1:1.

## O que está pronto

- API-Football como fonte dos jogos do dia.
- Filtro dos campeonatos configurados em `config.py`.
- Pesquisa de transmissão via Tavily em poucas fontes brasileiras confiáveis.
- Extração somente de canais/plataformas citados na evidência; se não houver confirmação, mostra `Transmissão não confirmada`.
- Cache de transmissão para reduzir custo e chamadas repetidas.
- Telegram com `/start`, `/jogos`, `/hoje`, `/stop` e `/ajuda`.
- Mensagens longas são divididas automaticamente para o Telegram.
- Webhook Telegram para produção, sem depender de `getUpdates`.
- WhatsApp Cloud API 1:1 com webhook e verificação opcional da assinatura Meta.
- Persistência local em JSON ou persistência em Supabase para produção/serverless.
- Vercel pronta para webhook HTTPS e cron diário.
- CI no GitHub para validar sintaxe a cada push.

## Teste local

```bash
python -m pip install -r requirements.txt
python agente_futebol.py
```

Para testar o servidor:

```bash
python app.py
```

Em outro terminal:

```bash
curl http://127.0.0.1:8000/health
```

## Variáveis de ambiente

Copie `.env.example` para `.env` e preencha as chaves. **Nunca envie `.env` para o GitHub.**

As mínimas para Telegram local são:

```env
API_FOOTBALL_KEY=
TAVILY_API_KEY=
TELEGRAM_BOT_TOKEN=
```

## Produção gratuita recomendada

### 1. GitHub

Crie um repositório para o projeto e envie os arquivos **sem `.env`**. O workflow `.github/workflows/ci.yml` valida o projeto a cada push.

### 2. Supabase (persistência)

Crie um projeto Supabase e execute `supabase_schema.sql` no SQL Editor. Depois configure no ambiente do deploy:

```env
SUPABASE_URL=
SUPABASE_KEY=
```

Use uma chave de servidor/segredo adequada ao backend. Não coloque essa chave no código ou no GitHub.

Sem Supabase, o projeto continua funcionando localmente com `usuarios.json`, mas ambientes serverless não devem depender de arquivo local persistente.

### 3. Vercel

Importe o repositório GitHub na Vercel. O runtime Python suporta Flask e o arquivo `api/index.py` expõe a aplicação.

Configure as variáveis de ambiente do `.env.example` no painel da Vercel. Depois do deploy, defina:

```env
APP_BASE_URL=https://SEU-PROJETO.vercel.app
TELEGRAM_USE_WEBHOOK=true
```

O `vercel.json` agenda `/cron/daily` uma vez por dia às **11:00 UTC (~08:00 de Brasília)**. No plano Hobby a execução diária pode ocorrer em qualquer momento dentro da hora programada.

Defina também um `CRON_SECRET` forte. A Vercel o envia como `Authorization: Bearer ...` para proteger o cron.

### 4. Telegram webhook

Depois que `APP_BASE_URL`, `TELEGRAM_BOT_TOKEN` e `TELEGRAM_WEBHOOK_SECRET` estiverem definidos localmente, rode:

```bash
python scripts/configurar_telegram_webhook.py
```

Depois disso o Telegram enviará `/start`, `/jogos` etc. diretamente para:

```text
https://SEU-PROJETO.vercel.app/webhook/telegram
```

Quando estiver usando webhook, mantenha:

```env
TELEGRAM_USE_WEBHOOK=true
```

Para voltar ao modo local `getUpdates`:

```bash
python scripts/remover_telegram_webhook.py
```

## WhatsApp Cloud API — mensagens 1:1

O código já possui:

```text
GET  /webhook/whatsapp   -> verificação do webhook
POST /webhook/whatsapp   -> recebimento de mensagens
```

Configure no ambiente:

```env
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_VERIFY_TOKEN=
META_APP_SECRET=
WHATSAPP_API_VERSION=v25.0
```

No painel Meta, o callback será:

```text
https://SEU-PROJETO.vercel.app/webhook/whatsapp
```

O valor de `WHATSAPP_VERIFY_TOKEN` é uma string que **você mesmo escolhe** e deve ser igual no painel Meta e nas variáveis do deploy.

O usuário pode mandar `jogos`, `jogos de hoje`, `hoje` ou `1` para receber o boletim.

### Importante sobre WhatsApp Channels

**WhatsApp Channels não são a mesma coisa que WhatsApp Business Cloud API 1:1.** Este projeto não inventa uma integração de Channels sem uma API oficial suportada e validada. A camada WhatsApp incluída aqui é para conversa direta com o número Business via Cloud API. A publicação automática em Channels deve ser tratada como uma etapa separada quando houver uma interface oficial disponível para a conta/caso de uso.

## Formato do boletim

```text
⚽ JOGOS DE HOJE
📅 14/09/2026

🏆 Serie A
⚽ Torino x Roma
🕐 13:30
📺 ESPN / Disney+

⚽ Como x Parma
🕐 13:30
📺 Transmissão não confirmada

🤖 Agente Futebol
```

Links e snippets brutos da busca **não são exibidos** no boletim principal.

## Segurança

- `.env`, `usuarios.json`, `estado_bot.json` e `transmissoes_cache.json` estão ignorados pelo Git.
- Credenciais devem ficar em Secrets/Environment Variables da plataforma.
- Como credenciais antigas já passaram por arquivos locais durante o desenvolvimento, rotacione tokens antes de publicar em produção.
- Não publique `SUPABASE_KEY`, `META_APP_SECRET`, tokens Telegram/WhatsApp ou chaves de APIs.

## Comandos Telegram

```text
/start  cadastra/reativa o usuário
/jogos  consulta o boletim agora
/hoje   alias de /jogos
/stop   desativa o envio diário
/ajuda  lista os comandos
```
