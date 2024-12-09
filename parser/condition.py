from typing import override
from interpreter.context import Context
from parser.expressible import Expressible

class Condition(Expressible):
    def __init__(self, v1: Expressible, op: str, v2: Expressible):
        self.v1: Expressible = v1
        self.op: str = op
        self.v2: Expressible = v2

    def __str__(self) -> str:
        return f'{self.v1} {self.op} {self.v2}'