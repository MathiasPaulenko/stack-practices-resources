# Runbook de Actualización de Dependencias — Simulación ejecutable

Companion del doc de StackPractices [Runbook de Actualización de Dependencias](https://stackpractices.com/es/docs/dependency-upgrade-template/).

Una simulación de las cinco fases del runbook en tres lenguajes. Cada script pasa dos actualizaciones de dependencias por el mismo checklist: una supera la validación y llega al merge con monitoreo, la otra falla en la fase de tests y ejercita el camino de reversión — restaurar el tag, instalación limpia, listo en menos de 15 minutos. Solo stdlib, sin dependencias.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/upgrade-runbook.js` | Node.js 18+ | `node src/upgrade-runbook.js` |
| `src/upgrade_runbook.py` | Python 3.9+ | `python src/upgrade_runbook.py` |
| `src/UpgradeRunbook.java` | Java 11+ | `javac -d src src/UpgradeRunbook.java && java -cp src UpgradeRunbook` |

Cada ejecución imprime el checklist por fase — preparación, actualización, validación, reversión, merge y monitoreo — para ver exactamente qué pasos promueven una actualización y cuáles disparan la reversión. Los nombres de tooling se localizan por stack (npm, pip-compile, mvn) como en un runbook real.
