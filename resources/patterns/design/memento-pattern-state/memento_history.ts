// Memento pattern — runnable TypeScript (Node >= 22.18, type stripping)
// Originator + Memento + Caretaker: text editor undo, game checkpoints,
// and a multi-step form wizard.

export interface Memento {
  getState(): string;
}

// ---------- Text editor (Originator + Caretaker) ----------

export class TextEditor {
  private content = '';
  private cursorPosition = 0;
  private selectionRange: [number, number] = [0, 0];

  type(text: string): void {
    const before = this.content.slice(0, this.cursorPosition);
    const after = this.content.slice(this.cursorPosition);
    this.content = before + text + after;
    this.cursorPosition += text.length;
    this.selectionRange = [this.cursorPosition, this.cursorPosition];
  }

  delete(): void {
    const [start, end] = this.selectionRange;
    if (start === end && start > 0) {
      this.content = this.content.slice(0, start - 1) + this.content.slice(start);
      this.cursorPosition = start - 1;
    } else {
      this.content = this.content.slice(0, start) + this.content.slice(end);
      this.cursorPosition = start;
    }
    this.selectionRange = [this.cursorPosition, this.cursorPosition];
  }

  save(): EditorSnapshot {
    return new EditorSnapshot(this.content, this.cursorPosition, this.selectionRange);
  }

  restore(memento: Memento): void {
    const snapshot = memento as EditorSnapshot;
    this.content = snapshot.getContent();
    this.cursorPosition = snapshot.getCursor();
    this.selectionRange = snapshot.getSelection();
  }

  getContent(): string {
    return this.content;
  }
}

export class EditorSnapshot implements Memento {
  private content: string;
  private cursor: number;
  private selection: [number, number];

  constructor(content: string, cursor: number, selection: [number, number]) {
    this.content = content;
    this.cursor = cursor;
    this.selection = selection;
  }

  getState(): string {
    return JSON.stringify({
      content: this.content,
      cursor: this.cursor,
      selection: this.selection,
    });
  }

  getContent(): string { return this.content; }
  getCursor(): number { return this.cursor; }
  getSelection(): [number, number] { return this.selection; }
}

export class EditorHistory {
  private history: Memento[] = [];
  private currentIndex = -1;

  backup(editor: TextEditor): void {
    // New edits after an undo drop the redo branch.
    this.history = this.history.slice(0, this.currentIndex + 1);
    this.history.push(editor.save());
    this.currentIndex++;
  }

  undo(editor: TextEditor): void {
    if (this.currentIndex <= 0) return;
    this.currentIndex--;
    editor.restore(this.history[this.currentIndex]);
  }

  redo(editor: TextEditor): void {
    if (this.currentIndex >= this.history.length - 1) return;
    this.currentIndex++;
    editor.restore(this.history[this.currentIndex]);
  }

  size(): number {
    return this.history.length;
  }
}

// ---------- Game checkpoint ----------

export class GameState {
  private level = 1;
  private health = 100;
  private inventory: string[] = [];

  addItem(item: string): void {
    this.inventory.push(item);
  }

  damage(amount: number): void {
    this.health = Math.max(0, this.health - amount);
  }

  createCheckpoint(): Memento {
    // Spread copies the array — the snapshot must not share it with live state.
    return new GameCheckpoint(this.level, this.health, [...this.inventory]);
  }

  loadCheckpoint(checkpoint: Memento): void {
    const cp = checkpoint as GameCheckpoint;
    this.level = cp.getLevel();
    this.health = cp.getHealth();
    this.inventory = cp.getInventory();
  }

  getHealth(): number { return this.health; }
  getInventory(): readonly string[] { return this.inventory; }
}

export class GameCheckpoint implements Memento {
  private level: number;
  private health: number;
  private inventory: string[];

  constructor(level: number, health: number, inventory: string[]) {
    this.level = level;
    this.health = health;
    this.inventory = inventory;
  }

  getState(): string {
    return JSON.stringify({ level: this.level, health: this.health });
  }

  getLevel(): number { return this.level; }
  getHealth(): number { return this.health; }
  getInventory(): string[] { return [...this.inventory]; }
}

// ---------- Multi-step form wizard ----------

export type FormState = {
  fields: Record<string, string>;
  errors: Record<string, string>;
  step: number;
};

// Separate shape from the `Memento` interface on purpose: this snapshot
// returns structured state, not a serialized string.
export class FormMemento {
  private state: FormState;

  constructor(state: FormState) {
    this.state = state;
  }
  getState(): FormState {
    // Copy on the way out too — callers must not mutate the stored state.
    return { ...this.state, fields: { ...this.state.fields }, errors: { ...this.state.errors } };
  }
  getRaw(): string {
    return JSON.stringify(this.state);
  }
}

export class FormEditor {
  private state: FormState = { fields: {}, errors: {}, step: 0 };

  setField(name: string, value: string): void {
    this.state.fields[name] = value;
  }
  setStep(step: number): void {
    this.state.step = step;
  }
  setErrors(errors: Record<string, string>): void {
    this.state.errors = errors;
  }

  save(): FormMemento {
    return new FormMemento({
      ...this.state,
      fields: { ...this.state.fields },
      errors: { ...this.state.errors },
    });
  }

  restore(memento: FormMemento): void {
    this.state = memento.getState();
  }

  getState(): FormState {
    return { ...this.state };
  }
}

export class FormHistory {
  private history: FormMemento[] = [];
  private maxHistory = 50;

  push(memento: FormMemento): void {
    this.history.push(memento);
    if (this.history.length > this.maxHistory) this.history.shift();
  }

  pop(): FormMemento | null {
    return this.history.pop() ?? null;
  }

  canRestore(): boolean {
    return this.history.length > 0;
  }
}

// ---------- Demo (runs on `node memento_history.ts`) ----------

const editor = new TextEditor();
const history = new EditorHistory();

history.backup(editor);
editor.type('Hello');
history.backup(editor);
editor.type(' World');

console.log(editor.getContent()); // "Hello World"
history.undo(editor);
console.log(editor.getContent()); // "Hello"
history.redo(editor);
console.log(editor.getContent()); // "Hello World"

const form = new FormEditor();
const formHistory = new FormHistory();
form.setField('email', 'user@test.com');
form.setStep(1);
formHistory.push(form.save());
form.setField('name', 'Alice');
form.setStep(2);

const prev = formHistory.pop();
if (prev) form.restore(prev);
console.log(form.getState().step); // 1
