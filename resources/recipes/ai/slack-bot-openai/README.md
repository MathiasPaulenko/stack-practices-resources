# Slack Bot with OpenAI

Runnable companion code for the recipe [Build a Slack Bot with OpenAI](https://stackpractices.com/recipes/slack-bot-openai/) on StackPractices.

## Contents

| File | Language | What it shows |
| --- | --- | --- |
| `app.js` | JavaScript | Bolt app in Socket Mode: `app_mention` handler with threaded replies, DM handler with `bot_id`/empty-text guards, per-user rolling history |
| `bot.py` | Python | Same flow with `slack-bolt` + `SocketModeHandler` |
| `tools.js` | JavaScript | Function calling: tool declaration, two-step completion with a stubbed `search_knowledge_base` tool |
| `.env.example` | — | Required tokens: `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_APP_TOKEN`, `OPENAI_API_KEY` |

## Run

```bash
# Node.js
npm install @slack/bolt openai dotenv
cp .env.example .env   # fill in your tokens
node app.js

# Python
pip install slack-bolt openai python-dotenv
cp .env.example .env   # fill in your tokens
python bot.py
```

You need a Slack app with Socket Mode enabled and an `xapp-` app-level token, plus a bot token with `app_mentions:read`, `chat:write`, and `im:history` scopes.
