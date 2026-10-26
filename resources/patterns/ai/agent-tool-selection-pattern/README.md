# Agent Tool Selection Pattern — Runnable Implementations

Companion to the StackPractices pattern [Agent Tool Selection Pattern](https://stackpractices.com/patterns/agent-tool-selection-pattern/).

A tool selector that narrows the full registry before each agent step: phase-based mapping, keyword matching, and a prompt formatter for the filtered tool definitions. Three equivalent implementations, stdlib only — no API keys needed.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/agent_tool_selection.py` | Python 3.10+ (stdlib only) | `python src/agent_tool_selection.py` |
| `src/agent-tool-selection.js` | Node.js 18+ (stdlib only) | `node src/agent-tool-selection.js` |
| `src/AgentToolSelection.java` | Java 17+ | `javac src/AgentToolSelection.java && java -cp src AgentToolSelection` |

Each run selects tools for a security-audit task in the `implementation` phase and prints the filtered set plus the formatted prompt lines — swap `strategy` between `phase`, `keyword` and `all` to see the difference.
