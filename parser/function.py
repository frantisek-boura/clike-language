from typing import override
from interpreter.context import Context
from parser.array_declaration import Array
from parser.datatype import Datatype
from parser.expressible import Expressible
from parser.function_parameter import FunctionParameter
from parser.statement import Statement

class Function(Statement):
    def __init__(self, name: str, datatype: Datatype, params: list[FunctionParameter], block: Statement):
        self.name: str = name
        self.datatype: Datatype = datatype
        self.params: list[FunctionParameter] = params
        self.block: Statement = block 
        self.value: Expressible | Array = None

    def __str__(self) -> str:
        return f'{self.datatype} {self.name} ({', '.join([str(p) for p in self.params])}) \n {self.block}'
