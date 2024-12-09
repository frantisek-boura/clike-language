from typing import override
from interpreter.context import Context
from parser.constant import Constant
from parser.function import Function
from parser.statement import Statement
from parser.variable import Variable

class Block(Statement):
    def __init__(self):
        self.variables: list[Variable] = [] 
        self.constants: list[Constant] = [] 
        self.functions: list[Function] = [] 
        self.statements: list[Statement] = [] 

    def __str__(self) -> str:
        result: str = ''
        result += '{\n'
        result += 'vars: \n' + ', '.join([str(v) for v in self.variables])
        result += '\n'
        result += 'consts: \n' + ', '.join([str(c) for c in self.constants])
        result += '\n'
        result += 'funcs: \n' + '\n'.join([str(f) for f in self.functions])
        result += '\n'
        result += 'statements: \n' + ';\n'.join([str(s) for s in self.statements])
        result += '}\n'
        return result