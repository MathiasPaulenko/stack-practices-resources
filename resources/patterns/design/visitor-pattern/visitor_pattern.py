"""Visitor pattern: an expression AST with eval and print visitors.

Classic real-world shape of the pattern — compilers, linters and exporters
all walk a stable node hierarchy while new operations get added as visitors.

No dependencies; run directly: python visitor_pattern.py
"""

from abc import ABC, abstractmethod


class ExprVisitor(ABC):
    """One visit method per concrete element type."""

    @abstractmethod
    def visit_number(self, node: "Number"):
        ...

    @abstractmethod
    def visit_add(self, node: "Add"):
        ...

    @abstractmethod
    def visit_mul(self, node: "Mul"):
        ...


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        ...


class Number(Expr):
    def __init__(self, value: float):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_number(self)


class Add(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_add(self)


class Mul(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_mul(self)


class EvalVisitor(ExprVisitor):
    """Computes the expression's numeric value."""

    def visit_number(self, node: Number) -> float:
        return node.value

    def visit_add(self, node: Add) -> float:
        return node.left.accept(self) + node.right.accept(self)

    def visit_mul(self, node: Mul) -> float:
        return node.left.accept(self) * node.right.accept(self)


class PrintVisitor(ExprVisitor):
    """Renders the expression back to infix notation."""

    def visit_number(self, node: Number) -> str:
        return str(node.value)

    def visit_add(self, node: Add) -> str:
        return f"({node.left.accept(self)} + {node.right.accept(self)})"

    def visit_mul(self, node: Mul) -> str:
        return f"({node.left.accept(self)} * {node.right.accept(self)})"


class CountNodesVisitor(ExprVisitor):
    """A third operation added without touching any Expr class."""

    def visit_number(self, node: Number) -> int:
        return 1

    def visit_add(self, node: Add) -> int:
        return 1 + node.left.accept(self) + node.right.accept(self)

    def visit_mul(self, node: Mul) -> int:
        return 1 + node.left.accept(self) + node.right.accept(self)


if __name__ == "__main__":
    # (2 + 3) * 4
    expr = Mul(Add(Number(2), Number(3)), Number(4))

    print(expr.accept(PrintVisitor()))
    # -> ((2 + 3) * 4)
    print(expr.accept(EvalVisitor()))
    # -> 20
    print(expr.accept(CountNodesVisitor()))
    # -> 5
