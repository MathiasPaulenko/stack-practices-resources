# Agentes de IA en Producción — Companion

Esqueletos ejecutables de la [Guía Completa de Agentes de IA en Producción](https://stackpractices.com/es/guides/complete-guide-ai-agents-production/).

## Archivos

- `react_agent.py` — bucle ReAct (razona/actúa/observa) con function calling y tope de iteraciones
- `plan_execute_agent.py` — separación planificador + ejecutor
- `supervisor_agent.py` — supervisor que delega en sub-agentes
- `collaborative_agents.py` — patrón de discusión/revisión multi-agente
- `short_term_memory.py` — memoria de conversación con ventana deslizante
- `long_term_memory.py` — memoria con vector store (ChromaDB + embeddings)
- `human_in_the_loop.py` — puerta de aprobación para llamadas irreversibles
- `safety_layer.py` — guardrails de entrada/salida y lista blanca de herramientas
- `agent_trace.py` — trazado estructurado (pensamientos, acciones, errores, resumen)

## Uso

Requiere `openai` (y `chromadb` para `long_term_memory.py`):

```bash
pip install openai chromadb
export OPENAI_API_KEY=...
python react_agent.py
```

Cada archivo es autocontenido. Adapta herramientas, modelos y presupuestos a tu stack; `run_code` debe ejecutarse en un sandbox, nunca en el mismo proceso.
