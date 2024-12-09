from typing import override
from interpreter.context import Context
from parser.array_declaration import Array
from parser.datatype import Datatype
from parser.expressible import Expressible
from parser.statement import Statement

class FunctionCall(Statement, Expressible):
    def __init__(self, name: str, datatype: Datatype, args: list[Expressible]):
        self.name: str = name
        self.datatype: Datatype = datatype
        self.args: list[Expressible] = args
        self.value: Expressible | Array = None
    
    def __str__(self) -> str:
        return f'{self.datatype} {self.name} ({', '.join([str(a) for a in self.args])})'