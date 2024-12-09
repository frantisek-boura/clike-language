from typing import override
from interpreter.context import Context
from parser.array_declaration import Array
from parser.assignable import Assignable
from parser.expressible import Expressible
from parser.datatype import Datatype
from parser.literal import Literal

class Variable(Expressible, Assignable):
    def __init__(self, name: str, datatype: Datatype):
        self.name: str = name 
        self.datatype: Datatype = datatype
        self.value: Expressible | Array = None 

    def __str__(self) -> str:
        return f'{self.datatype} {self.name}'