from parser.datatype import Datatype

class FunctionParameter:
    def __init__(self, name: str, datatype: Datatype):
        self.name: str = name
        self.datatype: Datatype = datatype

    def __str__(self) -> str:
        return f'{self.datatype} {self.name}'