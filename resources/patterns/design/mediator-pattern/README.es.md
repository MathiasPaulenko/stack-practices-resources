# Patrón Mediator — Recursos complementarios

Ejemplos ejecutables de la página del [Patrón Mediator](https://stackpractices.com/es/patterns/mediator-pattern/) en StackPractices.

| Archivo | Qué es |
|---------|--------|
| `src/chat_room.py` | Mediador de sala de chat en Python — los colegas (`User`) solo conocen la interfaz `ChatMediator` |
| `src/chat-room.js` | La misma sala en JavaScript plano — `node chat-room.js` |
| `src/ChatRoom.java` | Versión Java con `main` — un solo archivo que compila y corre |
| `src/checkout-wizard.ts` | Wizard de varios pasos: el mediador controla el flujo (next/back/complete) y los datos |

## La idea en una línea

N×N conexiones se convierten en N conexiones a un hub — la coordinación vive en un solo sitio, y el riesgo es que el hub crezca hasta ser un objeto dios.
