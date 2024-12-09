from typing import override
from interpreter.context import Context
from parser.datatype import Datatype
from parser.term import Term
from parser.expressible import Expressible

class Expression(Expressible):
    def __init__(self, op, terms: list[Term]):
        self.op: str = op
        self.terms: list[Term] = terms
        self.datatype: Datatype = None

    def __str__(self) -> str:
        return f'<{self.datatype if self.datatype != None else ''}>{self.op}({' '.join([str(t) for t in self.terms])})'
