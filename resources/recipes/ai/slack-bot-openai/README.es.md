# Bot de Slack con OpenAI

Código ejecutable complementario de la receta [Bot de Slack con OpenAI](https://stackpractices.com/es/recipes/slack-bot-openai/) en StackPractices.

## Contenido

| Archivo | Lenguaje | Qué muestra |
| --- | --- | --- |
| `app.js` | JavaScript | App Bolt en Socket Mode: handler de `app_mention` con respuestas en hilo, handler de DMs con guardas de `bot_id`/texto vacío, historial móvil por usuario |
| `bot.py` | Python | El mismo flujo con `slack-bolt` + `SocketModeHandler` |
| `tools.js` | JavaScript | Function calling: declaración de tools, completion en dos pasos con una tool `search_knowledge_base` de ejemplo |
| `.env.example` | — | Tokens necesarios: `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_APP_TOKEN`, `OPENAI_API_KEY` |

## Ejecutar

```bash
# Node.js
npm install @slack/bolt openai dotenv
cp .env.example .env   # completa tus tokens
node app.js

# Python
pip install slack-bolt openai python-dotenv
cp .env.example .env   # completa tus tokens
python bot.py
```

Necesitas una app de Slack con Socket Mode habilitado y un token de nivel app `xapp-`, además de un bot token con los scopes `app_mentions:read`, `chat:write` e `im:history`.
