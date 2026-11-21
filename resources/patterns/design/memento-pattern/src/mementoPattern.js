// Memento pattern — text editor undo stack (no dependencies, Node 18+).
// Originator (TextEditor) produces frozen snapshots (EditorMemento);
// the Caretaker (History) stores them without reading their contents.

class EditorMemento {
  constructor(content, cursor, version = 1) {
    // Freeze so neither the caretaker nor a stray bug can rewrite history.
    this._state = Object.freeze({ content, cursor, version });
  }
}

class TextEditor {
  static SCHEMA_VERSION = 1;

  constructor() {
    this._content = "";
    this._cursor = 0;
  }

  type(text) {
    this._content =
      this._content.slice(0, this._cursor) +
      text +
      this._content.slice(this._cursor);
    this._cursor += text.length;
  }

  moveCursor(position) {
    this._cursor = Math.max(0, Math.min(position, this._content.length));
  }

  save() {
    return new EditorMemento(this._content, this._cursor, TextEditor.SCHEMA_VERSION);
  }

  restore(memento) {
    if (memento._state.version !== TextEditor.SCHEMA_VERSION) {
      throw new Error(`Unsupported memento version ${memento._state.version}`);
    }
    this._content = memento._state.content;
    this._cursor = memento._state.cursor;
  }

  get content() {
    return this._content;
  }
}

class History {
  constructor(limit = 50) {
    this.stack = [];
    this.limit = limit;
  }

  push(memento) {
    this.stack.push(memento);
    if (this.stack.length > this.limit) this.stack.shift();
  }

  pop() {
    return this.stack.pop() ?? null;
  }

  get size() {
    return this.stack.length;
  }
}

if (require.main === module) {
  const editor = new TextEditor();
  const history = new History();

  history.push(editor.save());
  editor.type("Hello ");
  history.push(editor.save());
  editor.type("World!");

  console.log(editor.content); // Hello World!

  editor.restore(history.pop());
  console.log(editor.content); // "Hello "

  editor.restore(history.pop());
  console.log(JSON.stringify(editor.content)); // ""

  editor.type("ab");
  editor.type("ef");
  editor.moveCursor(2);
  editor.type("cd");
  console.log(editor.content); // abcdef
}

module.exports = { EditorMemento, TextEditor, History };
