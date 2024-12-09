from typing import override
from interpreter.context import Context
from parser.assign_statement import AssignStatement
from parser.block import Block
from parser.condition import Condition
from parser.statement import Statement
from parser.variable import Variable

class ForStatement(Statement):
    def __init__(self):
        self.variable: Variable = None 
        self.starting_assign: AssignStatement = None 
        self.condition: Condition = None 
        self.iter_assign: AssignStatement = None
        self.block: Block = None 

    def __str__(self) -> str:
        return f'for ({self.variable} ({self.starting_assign}) ; {self.condition} ; {self.iter_assign}) \n {self.block}'