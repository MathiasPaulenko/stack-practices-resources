# Patrón Prompt Chaining — Recursos Companion

Archivos companion del [Patrón Prompt Chaining](https://stackpractices.com/es/patterns/prompt-chaining-pattern/) en StackPractices.com.

## Qué incluye

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `prompt_chain.py` | Python | Clase `PromptChain` con dataclass `ChainStep`, validadores, lógica de reintentos |
| `prompt_chain.js` | JavaScript | Clase `PromptChain` con `run()` async, validadores, lógica de reintentos |
| `PromptChaining.java` | Java | `PromptChaining` con records `ChainStep`/`ChainResult`, validadores `Predicate` |

## Inicio rápido

### Python

```bash
python prompt_chain.py
```

### JavaScript

```bash
node prompt_chain.js
```

### Java

```bash
javac PromptChaining.java && java PromptChaining
```

## Cómo funciona

1. Define pasos de cadena con nombre, plantilla de prompt, modelo, temperatura y validador opcional
2. La cadena ejecuta pasos secuencialmente: la salida de cada paso alimenta la entrada del siguiente
3. Si el validador de un paso falla, el paso reintenta hasta `max_retries` veces
4. Si todos los reintentos fallan, la cadena se detiene y devuelve resultados parciales

## Reemplazar el mock

La función `mock_llm_call` / `mockLlmCall` simula una llamada al LLM. Reemplázala con tu cliente real:

- **Python**: `openai.chat.completions.create()` o `anthropic.messages.create()`
- **JavaScript**: `openai.chat.completions.create()` o `@anthropic-ai/sdk`
- **Java**: OpenAI Java SDK o Anthropic Java SDK

## Referencias

- [Guía de prompt engineering de OpenAI](https://platform.openai.com/docs/guides/prompt-engineering)
- [Documentación de chains de LangChain](https://python.langchain.com/docs/modules/chains/)
- [Guía de chain prompts de Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts)
