from typing import override
from interpreter.context import Context
from parser.array_declaration import Array
from parser.expressible import Expressible
from parser.statement import Statement

class ReturnStatement(Statement):
    def __init__(self, value: Expressible):
        self.value: Expressible | Array = value

    def __str__(self) -> str:
        return f'return {self.value}'