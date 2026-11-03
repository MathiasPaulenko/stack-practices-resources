# Command Pattern — Companion Files

Companion to the StackPractices pattern [Command Pattern](https://stackpractices.com/patterns/command-pattern/).

| File | Contains |
|---|---|
| src/command_queue.py | Full Python example: Command ABC, EmailService receiver, SendEmailCommand, JobQueue invoker with history and cancel |
| src/command_queue.js | Same example in JavaScript |
| src/CommandQueue.java | Same example in Java (interface + concrete command + invoker) |

## Usage

Each file is self-contained: the client wires commands to receivers and submits them to the queue. Run `python src/command_queue.py`, `node src/command_queue.js`, or compile `CommandQueue.java` to see execute/undo in action.
