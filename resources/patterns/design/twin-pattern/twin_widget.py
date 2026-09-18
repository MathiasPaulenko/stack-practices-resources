"""Twin Pattern — runnable example.

A ``Widget`` keeps the shared state and the public API. ``Graphic`` and
``Interactive`` are the twins: each owns one concern and holds a
back-reference to the widget so it can read shared state.

Run the demo:

    python twin_widget.py

Run the tests:

    python -m unittest twin_widget -v
"""

from __future__ import annotations

import unittest
from typing import Optional, Protocol


class WidgetLike(Protocol):
    """Minimal surface a twin needs from its widget.

    Injecting this interface (instead of the concrete Widget) is what
    makes twins unit-testable: a stub with the same fields is enough.
    """

    name: str
    x: int
    y: int
    width: int
    height: int


class Graphic:
    """Twin A: drawing behavior."""

    def __init__(self) -> None:
        self.widget: Optional[WidgetLike] = None

    def draw(self) -> str:
        w = self._linked()
        return f"Drawing {w.name} at ({w.x}, {w.y})"

    def resize(self, width: int, height: int) -> str:
        w = self._linked()
        w.width = width
        w.height = height
        return f"Resized to {width}x{height}"

    def _linked(self) -> WidgetLike:
        if self.widget is None:
            raise RuntimeError("Graphic twin is not linked to a widget")
        return self.widget


class Interactive:
    """Twin B: interaction behavior."""

    def __init__(self) -> None:
        self.widget: Optional[WidgetLike] = None

    def on_click(self) -> str:
        return f"Clicked on {self._linked().name}"

    def on_hover(self) -> str:
        return f"Hovering over {self._linked().name}"

    def _linked(self) -> WidgetLike:
        if self.widget is None:
            raise RuntimeError("Interactive twin is not linked to a widget")
        return self.widget


class Widget:
    """The composite twin class that links Graphic and Interactive."""

    def __init__(self, name: str, x: int = 0, y: int = 0) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.width = 100
        self.height = 50

        self._graphic = Graphic()
        self._graphic.widget = self
        self._interactive = Interactive()
        self._interactive.widget = self

    def draw(self) -> str:
        return self._graphic.draw()

    def resize(self, width: int, height: int) -> str:
        return self._graphic.resize(width, height)

    def on_click(self) -> str:
        return self._interactive.on_click()

    def on_hover(self) -> str:
        return self._interactive.on_hover()

    def get_graphic(self) -> Graphic:
        return self._graphic

    def get_interactive(self) -> Interactive:
        return self._interactive


class _FakeWidget:
    """Stub used to test a twin without a real Widget."""

    name = "Fake"
    x = 0
    y = 0
    width = 0
    height = 0


class TestTwinPattern(unittest.TestCase):
    def test_widget_delegates_to_twins(self) -> None:
        w = Widget("SubmitButton", 10, 20)
        self.assertEqual(w.draw(), "Drawing SubmitButton at (10, 20)")
        self.assertEqual(w.on_click(), "Clicked on SubmitButton")
        w.resize(200, 60)
        self.assertEqual((w.width, w.height), (200, 60))

    def test_twin_is_testable_with_a_stub(self) -> None:
        g = Graphic()
        g.widget = _FakeWidget()
        self.assertEqual(g.draw(), "Drawing Fake at (0, 0)")

    def test_unlinked_twin_fails_fast(self) -> None:
        with self.assertRaises(RuntimeError):
            Graphic().draw()

    def test_twin_can_be_swapped(self) -> None:
        w = Widget("Btn")
        custom = Graphic()
        custom.widget = w
        w._graphic = custom
        self.assertIs(w.get_graphic(), custom)


if __name__ == "__main__":
    button = Widget("SubmitButton", 10, 20)
    print(button.draw())
    print(button.on_click())
    print(button.on_hover())
    print(button.resize(200, 60))
