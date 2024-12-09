from typing import override
from interpreter.context import Context
from parser.literal import Literal

class IntLiteral(Literal):
    def __init__(self, value: int):
        self.value: int = value

    def __str__(self) -> str:
        return str(self.value)