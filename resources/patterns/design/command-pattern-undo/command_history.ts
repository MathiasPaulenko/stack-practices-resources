// Command pattern with undo/redo — runnable TypeScript (Node >= 22.18, type stripping)

export interface Command {
  execute(): void;
  undo(): void;
  getName(): string;
}

export interface AsyncCommand {
  execute(): Promise<void>;
  undo(): Promise<void>;
  getName(): string;
}

// Receiver — no history, no undo logic, just mutations
export class TextDocument {
  private content = '';

  insert(text: string, position: number): void {
    this.content =
      this.content.slice(0, position) + text + this.content.slice(position);
  }

  delete(position: number, length: number): string {
    const removed = this.content.slice(position, position + length);
    this.content =
      this.content.slice(0, position) + this.content.slice(position + length);
    return removed;
  }

  getContent(): string {
    return this.content;
  }
}

export class InsertCommand implements Command {
  private document: TextDocument;
  private text: string;
  private position: number;

  constructor(document: TextDocument, text: string, position: number) {
    this.document = document;
    this.text = text;
    this.position = position;
  }

  execute(): void {
    this.document.insert(this.text, this.position);
  }

  undo(): void {
    this.document.delete(this.position, this.text.length);
  }

  getName(): string {
    return `Insert "${this.text}"`;
  }
}

export class DeleteCommand implements Command {
  private document: TextDocument;
  private position: number;
  private length: number;
  private deletedText = '';

  constructor(document: TextDocument, position: number, length: number) {
    this.document = document;
    this.position = position;
    this.length = length;
  }

  execute(): void {
    this.deletedText = this.document.delete(this.position, this.length);
  }

  undo(): void {
    this.document.insert(this.deletedText, this.position);
  }

  getName(): string {
    return `Delete ${this.length} chars`;
  }
}

// Invoker — two stacks; a new action always discards the redo stack
export class CommandHistory {
  private undoStack: Command[] = [];
  private redoStack: Command[] = [];

  private maxHistory: number;

  constructor(maxHistory = Infinity) {
    this.maxHistory = maxHistory;
  }

  execute(command: Command): void {
    command.execute();
    this.undoStack.push(command);
    if (this.undoStack.length > this.maxHistory) this.undoStack.shift();
    this.redoStack = [];
  }

  undo(): void {
    const command = this.undoStack.pop();
    if (!command) return;
    command.undo();
    this.redoStack.push(command);
  }

  redo(): void {
    const command = this.redoStack.pop();
    if (!command) return;
    command.execute();
    this.undoStack.push(command);
  }

  canUndo(): boolean {
    return this.undoStack.length > 0;
  }

  canRedo(): boolean {
    return this.redoStack.length > 0;
  }
}

// Groups commands into a single undoable unit; undo runs in reverse order
export class MacroCommand implements Command {
  private commands: Command[];

  constructor(commands: Command[]) {
    this.commands = commands;
  }

  execute(): void {
    for (const command of this.commands) command.execute();
  }

  undo(): void {
    for (const command of [...this.commands].reverse()) command.undo();
  }

  getName(): string {
    return `Macro of ${this.commands.length} commands`;
  }
}

// Sequential queue for async work — overlapping executes would reorder history
export class CommandQueue {
  private undoStack: AsyncCommand[] = [];
  private pending: Promise<void> = Promise.resolve();

  execute(command: AsyncCommand): Promise<void> {
    const run = this.pending.then(async () => {
      await command.execute();
      this.undoStack.push(command);
    });
    this.pending = run;
    return run;
  }

  async undo(): Promise<void> {
    const command = this.undoStack.pop();
    if (command) await command.undo();
  }
}

// Demo
if (process.argv[1]?.endsWith('command_history.ts')) {
  const doc = new TextDocument();
  const history = new CommandHistory();

  history.execute(new InsertCommand(doc, 'Hello', 0));
  history.execute(new InsertCommand(doc, ' World', 5));
  console.log(doc.getContent()); // "Hello World"

  history.undo();
  console.log(doc.getContent()); // "Hello"

  history.redo();
  console.log(doc.getContent()); // "Hello World"

  // Macro: two edits become a single undo step
  const doc2 = new TextDocument();
  const history2 = new CommandHistory();
  history2.execute(
    new MacroCommand([
      new InsertCommand(doc2, 'a', 0),
      new InsertCommand(doc2, 'b', 1),
    ]),
  );
  console.log(doc2.getContent()); // "ab"
  history2.undo();
  console.log(doc2.getContent()); // ""
}
