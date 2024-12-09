from typing import override
from interpreter.context import Context
from parser.array_declaration import Array
from parser.array_element import ArrayElement
from parser.assignable import Assignable
from parser.expressible import Expressible
from parser.statement import Statement
from parser.variable import Variable

class AssignStatement(Statement):
    def __init__(self, assignable: Assignable, value: Expressible):
        self.assignable: Assignable = assignable
        self.value: Expressible | Array = value

    def __str__(self) -> str:
        return f'{self.assignable} = {self.value}'