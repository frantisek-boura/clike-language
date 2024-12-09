from typing import override
from interpreter.context import Context
from parser.condition import Condition
from parser.block import Block
from parser.statement import Statement

class IfStatement(Statement):
    def __init__(self):
        self.condition: Condition = None 
        self.block: Block = None 
        self.else_ifs: list[Statement] = [] 
        self.else_block: Block = None 

    def __str__(self) -> str:
        result: str = ''
        result += 'if '
        result += f'({self.condition}) \n'
        result += str(self.block)
        result += '\n'.join([str(e) for e in self.else_ifs])
        if self.else_block != None:
            result += '\n' + str(self.else_block)
        return result