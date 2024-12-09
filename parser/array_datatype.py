from parser.datatype import Datatype

class ArrayDatatype(Datatype):
    def __init__(self, name: str, dimensions: int):
        super().__init__(name)
        self.dimensions: int = dimensions 
    
    def __str__(self) -> str:
        return f'{self.name}{'[]' * self.dimensions}'