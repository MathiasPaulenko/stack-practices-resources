# chatbot-openai — Recursos complementarios

Código complementario para [Chatbot con OpenAI Assistants API: Build, Coste y Deploy](https://stackpractices.com/es/recipes/chatbot-openai/).

## Archivos

| Archivo | Lenguaje | Propósito |
|---------|----------|-----------|
| `chatbot.py` | Python | Loop de conversación completo con function calling |
| `chatbot.js` | JavaScript | El mismo bot en Node.js |
| `chatbot.java` | Java | Creación del assistant con el SDK oficial |
| `function_handler.py` | Python | Validación, manejo de errores y guard de reintentos |

## Requisitos

- Python 3.10+ o Node.js 18+ o Java 17+
- Variable de entorno `OPENAI_API_KEY`

## Inicio rápido

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

## Notas

- La Assistants API está deprecada (agosto 2025) y cierra el 26 de agosto de 2026.
- Reemplazá `vs_...` con tu vector store ID real.
- Reemplazá `get_order_status` con tu función de backend real.
- `function_handler.py` muestra validación y manejo de errores estructurado.
