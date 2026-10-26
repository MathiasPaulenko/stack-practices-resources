# Patrón Agent Tool Selection — Implementaciones ejecutables

Compañero del patrón de StackPractices [Patrón Agent Tool Selection](https://stackpractices.com/es/patterns/agent-tool-selection-pattern/).

Un selector que reduce el registro completo antes de cada paso del agente: mapeo por fase, coincidencia por palabras clave y formateo de las definiciones filtradas para el prompt. Tres implementaciones equivalentes, solo stdlib — sin API keys.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/agent_tool_selection.py` | Python 3.10+ (solo stdlib) | `python src/agent_tool_selection.py` |
| `src/agent-tool-selection.js` | Node.js 18+ (solo stdlib) | `node src/agent-tool-selection.js` |
| `src/AgentToolSelection.java` | Java 17+ | `javac src/AgentToolSelection.java && java -cp src AgentToolSelection` |

Cada ejecución selecciona herramientas para una tarea de auditoría de seguridad en la fase `implementation` e imprime el conjunto filtrado y las líneas del prompt — cambia `strategy` entre `phase`, `keyword` y `all` para ver la diferencia.
