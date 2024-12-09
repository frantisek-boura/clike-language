from parser.factor import Factor

class Term:
    def __init__(self, op: str, factors: list[Factor]):
        self.op: str = op
        self.factors: list[Factor] = factors

    def __str__(self) -> str:
        return f'{self.op}({' '.join([str(f) for f in self.factors])})'