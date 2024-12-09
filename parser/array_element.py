from typing import Any, override
from interpreter.context import Context
from parser.assignable import Assignable
from parser.datatype import Datatype
from parser.expressible import Expressible

class ArrayElement(Expressible, Assignable):
    def __init__(self, name: str, datatype: Datatype, indices: list[Expressible]):
        self.name: str = name
        self.datatype: Datatype = datatype
        self.indices: list[Expressible] = indices
        self.value: Expressible | list = None

    def __str__(self) -> str:
        return f'{self.datatype} {self.name}{[f'[{str(i)}]' for i in self.indices]}'