# Patrón Command — Archivos Companion

Companion del patrón de StackPractices [Patrón Command](https://stackpractices.com/es/patterns/command-pattern/).

| Archivo | Contiene |
|---|---|
| src/command_queue.py | Ejemplo completo en Python: ABC Command, receiver EmailService, SendEmailCommand, invoker JobQueue con historial y cancelación |
| src/command_queue.js | El mismo ejemplo en JavaScript |
| src/CommandQueue.java | El mismo ejemplo en Java (interfaz + comando concreto + invoker) |

## Uso

Cada archivo es autocontenido: el cliente conecta comandos a receivers y los envía a la cola. Ejecuta `python src/command_queue.py`, `node src/command_queue.js` o compila `CommandQueue.java` para ver el execute/undo en acción.
