"""Interpreter pattern: arithmetic expression language.

Build an AST of Expression nodes and evaluate it against a context.
Run: python interpreter_pattern.py
"""
from abc import ABC, abstractmethod
from typing import Any


class Expression(ABC):
    @abstractmethod
    def interpret(self, context: dict) -> Any:
        pass


class Number(Expression):
    def __init__(self, value: float):
        self.value = value

    def interpret(self, context: dict) -> float:
        return self.value


class Variable(Expression):
    def __init__(self, name: str):
        self.name = name

    def interpret(self, context: dict) -> Any:
        return context.get(self.name, 0)


class Add(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, context: dict) -> float:
        return self.left.interpret(context) + self.right.interpret(context)


class Subtract(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, context: dict) -> float:
        return self.left.interpret(context) - self.right.interpret(context)


if __name__ == "__main__":
    # Evaluate "(10 + x) - 5" where x = 3
    expression = Subtract(Add(Number(10), Variable("x")), Number(5))
    print(expression.interpret({"x": 3}))  # 8
