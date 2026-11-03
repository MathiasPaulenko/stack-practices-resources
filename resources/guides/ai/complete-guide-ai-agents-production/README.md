# AI Agents in Production — Companion

Runnable skeletons from the [Complete Guide to AI Agents in Production](https://stackpractices.com/guides/complete-guide-ai-agents-production/).

## Files

- `react_agent.py` — ReAct loop (reason/act/observe) with function calling and iteration cap
- `plan_execute_agent.py` — planner + executor separation
- `supervisor_agent.py` — supervisor delegating to sub-agents
- `collaborative_agents.py` — multi-agent discussion/review pattern
- `short_term_memory.py` — sliding-window conversation memory
- `long_term_memory.py` — vector-store memory with ChromaDB + embeddings
- `human_in_the_loop.py` — approval gate for irreversible tool calls
- `safety_layer.py` — input/output guardrails and tool allowlist
- `agent_trace.py` — structured run tracing (thoughts, actions, errors, summary)

## Usage

Requires `openai` (and `chromadb` for `long_term_memory.py`):

```bash
pip install openai chromadb
export OPENAI_API_KEY=...
python react_agent.py
```

Each file is self-contained. Adapt tools, models, and budgets to your stack; `run_code` must run in a sandbox, never in-process.
