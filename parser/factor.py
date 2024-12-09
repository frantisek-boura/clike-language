from parser.expressible import Expressible

class Factor:
    def __init__(self, op: str, value: Expressible):
        self.op: str = op
        self.value: Expressible = value

    def __str__(self) -> str:
        return f'{self.op if self.op != None else ''}({self.value})<{str(type(self.value))}>'