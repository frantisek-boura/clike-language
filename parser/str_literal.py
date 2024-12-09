from typing import override
from interpreter.context import Context
from parser.literal import Literal

class StrLiteral(Literal):
    def __init__(self, value: str):
        self.value: str = value.replace('"','')

    def __str__(self) -> str:
        return self.value