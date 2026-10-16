"""Companion code for "Visitor Pattern: Extensible Operations in TypeScript".

Python port of the TypeScript AST visitors from
https://stackpractices.com/patterns/visitor-pattern-operations/

Run: python visitor_ast.py  (Python 3.9+, no dependencies)
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any


class ASTVisitor(ABC):
    @abstractmethod
    def visit_number(self, node: "NumberNode") -> None: ...

    @abstractmethod
    def visit_binary_op(self, node: "BinaryOpNode") -> None: ...

    @abstractmethod
    def visit_variable(self, node: "VariableNode") -> None: ...


class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor: ASTVisitor) -> None: ...


class NumberNode(ASTNode):
    def __init__(self, value: float):
        self.value = value

    def accept(self, visitor: ASTVisitor) -> None:
        visitor.visit_number(self)


class BinaryOpNode(ASTNode):
    def __init__(self, operator: str, left: ASTNode, right: ASTNode):
        self.operator = operator
        self.left = left
        self.right = right

    def accept(self, visitor: ASTVisitor) -> None:
        visitor.visit_binary_op(self)


class VariableNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor: ASTVisitor) -> None:
        visitor.visit_variable(self)


class Evaluator(ASTVisitor):
    """Accumulates results on an internal stack."""

    def __init__(self, variables: dict[str, float]):
        self.variables = variables
        self.stack: list[float] = []

    def visit_number(self, node: NumberNode) -> None:
        self.stack.append(node.value)

    def visit_variable(self, node: VariableNode) -> None:
        self.stack.append(self.variables.get(node.name, 0))

    def visit_binary_op(self, node: BinaryOpNode) -> None:
        node.left.accept(self)
        node.right.accept(self)
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(
            {
                "+": left + right,
                "-": left - right,
                "*": left * right,
                "/": left / right,
            }[node.operator]
        )

    def get_result(self) -> float:
        return self.stack[-1]


class Printer(ASTVisitor):
    def __init__(self):
        self.output = ""

    def visit_number(self, node: NumberNode) -> None:
        self.output += str(node.value)

    def visit_variable(self, node: VariableNode) -> None:
        self.output += node.name

    def visit_binary_op(self, node: BinaryOpNode) -> None:
        self.output += "("
        node.left.accept(self)
        self.output += f" {node.operator} "
        node.right.accept(self)
        self.output += ")"

    def get_output(self) -> str:
        return self.output


class JSONSerializer(ASTVisitor):
    """Captures self.result between child traversals."""

    def __init__(self):
        self.result: Any = None

    def visit_number(self, node: NumberNode) -> None:
        self.result = {"type": "number", "value": node.value}

    def visit_variable(self, node: VariableNode) -> None:
        self.result = {"type": "variable", "name": node.name}

    def visit_binary_op(self, node: BinaryOpNode) -> None:
        node.left.accept(self)
        left = self.result
        node.right.accept(self)
        right = self.result
        self.result = {
            "type": "binaryOp",
            "operator": node.operator,
            "left": left,
            "right": right,
        }

    def serialize(self) -> str:
        return json.dumps(self.result)


if __name__ == "__main__":
    # AST for 2 + (x * 3)
    ast = BinaryOpNode(
        "+",
        NumberNode(2),
        BinaryOpNode("*", VariableNode("x"), NumberNode(3)),
    )

    evaluator = Evaluator({"x": 4})
    ast.accept(evaluator)
    print("eval:", evaluator.get_result())  # 14

    printer = Printer()
    ast.accept(printer)
    print("print:", printer.get_output())  # (2 + (x * 3))

    serializer = JSONSerializer()
    ast.accept(serializer)
    print("json:", serializer.serialize())
