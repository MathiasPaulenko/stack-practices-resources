# Componer cadenas LCEL en LangChain — Proyecto Companion

Companion ejecutable de la [receta de cadenas LCEL](https://stackpractices.com/es/recipes/python-langchain-chains-composition/) en StackPractices. Muestra cómo organizar las cadenas en varios archivos, algo que la FAQ de la receta menciona sin dar la estructura completa del proyecto.

## Contenido

| Archivo | Qué es |
|---------|--------|
| `chains.py` | Factories de cadenas: `basic_chain`, `summarize_then_translate_chain`, `parallel_analysis_chain`, `custom_components_chain`, `resilient_chain` (retry + fallback), `routing_chain`. Cada una devuelve un `Runnable` que puedes encadenar o importar en otro lado. |
| `main.py` | Punto de entrada que invoca cada variante de cadena, incluido un ejemplo de `batch`. |
| `requirements.txt` | `langchain`, `langchain-openai`, `langchain-core`, `pydantic`. |

## Ejecútalo

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python main.py
```

Adapta los nombres de modelos y los prompts a tu proveedor. Cualquier `BaseChatModel` sirve: Anthropic, Google o modelos locales vía `langchain-ollama`.

Receta fuente: https://stackpractices.com/es/recipes/python-langchain-chains-composition/
