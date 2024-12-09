from typing import override
from interpreter.context import Context
from parser.datatype import Datatype
from parser.expressible import Expressible
from parser.literal import Literal

class Constant(Expressible):
    def __init__(self, name: str, datatype: Datatype, value: Literal):
        self.name: str = name
        self.datatype: Datatype = datatype
        self.value: Literal = value

    def __str__(self) -> str:
        return f'{self.datatype} {self.name} = {self.value}'