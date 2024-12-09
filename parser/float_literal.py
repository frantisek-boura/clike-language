from typing import override
from interpreter.context import Context
from parser.literal import Literal

class FloatLiteral(Literal):
    def __init__(self, value: float):
        self.value: float = value

    def __str__(self) -> str:
        return str(self.value)