# Mediator Pattern — Companion Resources

Runnable examples for the [Mediator Pattern](https://stackpractices.com/patterns/mediator-pattern/) page on StackPractices.

| File | What it is |
|------|------------|
| `src/chat_room.py` | Chat room mediator in Python — colleagues (`User`) only know the `ChatMediator` interface |
| `src/chat-room.js` | Same chat room in plain JavaScript — `node chat-room.js` |
| `src/ChatRoom.java` | Java version with a `main` — one file that compiles and runs |
| `src/checkout-wizard.ts` | Multi-step wizard: the mediator owns flow (next/back/complete) and collected data |

## The idea in one line

N×N connections become N connections to a hub — coordination lives in one place, and the risk is the hub growing into a god object.
