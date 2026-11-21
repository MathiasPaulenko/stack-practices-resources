"""Memento pattern — text editor undo stack.

Originator (TextEditor) produces opaque snapshots (EditorMemento);
the Caretaker (History) stores them without reading their contents.
"""

from __future__ import annotations


class EditorMemento:
    """Opaque snapshot; only the originator reads its fields."""

    __slots__ = ("_content", "_cursor", "_version")

    def __init__(self, content: str, cursor: int, version: int = 1):
        self._content = content
        self._cursor = cursor
        self._version = version


class TextEditor:
    SCHEMA_VERSION = 1

    def __init__(self):
        self._content = ""
        self._cursor = 0

    def type(self, text: str) -> None:
        self._content = (
            self._content[: self._cursor] + text + self._content[self._cursor :]
        )
        self._cursor += len(text)

    def move_cursor(self, position: int) -> None:
        self._cursor = max(0, min(position, len(self._content)))

    def save(self) -> EditorMemento:
        return EditorMemento(self._content, self._cursor, self.SCHEMA_VERSION)

    def restore(self, memento: EditorMemento) -> None:
        if memento._version != self.SCHEMA_VERSION:
            raise ValueError(f"Unsupported memento version {memento._version}")
        self._content = memento._content
        self._cursor = memento._cursor

    @property
    def content(self) -> str:
        return self._content

    @property
    def cursor(self) -> int:
        return self._cursor


class History:
    """Caretaker: bounded stack of mementos it never inspects."""

    def __init__(self, limit: int = 50):
        self._stack: list[EditorMemento] = []
        self._limit = limit

    def push(self, memento: EditorMemento) -> None:
        self._stack.append(memento)
        if len(self._stack) > self._limit:
            self._stack.pop(0)

    def pop(self) -> EditorMemento | None:
        return self._stack.pop() if self._stack else None

    def __len__(self) -> int:
        return len(self._stack)


if __name__ == "__main__":
    editor = TextEditor()
    history = History()

    history.push(editor.save())
    editor.type("Hello ")
    history.push(editor.save())
    editor.type("World!")

    print(editor.content)  # Hello World!

    editor.restore(history.pop())
    print(editor.content)  # "Hello " — snapshot taken before typing World!

    editor.restore(history.pop())
    print(repr(editor.content))  # ''

    # Insert mid-text keeps the tail
    editor.type("ab")
    editor.type("ef")
    editor.move_cursor(2)
    editor.type("cd")
    print(editor.content)  # abcdef
