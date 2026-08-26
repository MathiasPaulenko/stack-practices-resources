# chatbot-openai — Companion Resources

Companion code for [OpenAI Assistants API Chatbot: Build, Cost & Deploy](https://stackpractices.com/recipes/chatbot-openai/).

## Files

| File | Language | Purpose |
|------|----------|---------|
| `chatbot.py` | Python | Full conversation loop with function calling |
| `chatbot.js` | JavaScript | Same bot in Node.js |
| `chatbot.java` | Java | Assistant creation with the official SDK |
| `function_handler.py` | Python | Validation, error handling, retry guard |

## Requirements

- Python 3.10+ or Node.js 18+ or Java 17+
- `OPENAI_API_KEY` environment variable

## Quick start

### Python

```bash
pip install openai
export OPENAI_API_KEY="sk-..."
python chatbot.py
```

### JavaScript

```bash
npm install openai
export OPENAI_API_KEY="sk-..."
node chatbot.js
```

## Notes

- The Assistants API is deprecated (August 2025) and shuts down on 26 August 2026.
- Replace `vs_...` with your actual vector store ID.
- Replace `get_order_status` with your real backend function.
- The `function_handler.py` shows validation and structured error handling.
