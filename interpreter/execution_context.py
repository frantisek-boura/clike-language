from copy import deepcopy
from typing import Any
from semantics.lib_functions import functions
from interpreter.context import Context
from parser.array_declaration import Array
from parser.block import Block
from parser.constant import Constant
from parser.expression import Expression
from parser.function import Function
from parser.function_call import FunctionCall
from parser.variable import Variable

class ExecutionContext(Context):
    def __init__(self, variables: list[Variable], constants: list[Constant], functions: list[Function], prior_context: Context = None):
        self.variables: list[Variable] = deepcopy(variables)
        self.constants: list[Constant] = deepcopy(constants)
        self.functions: list[Function] = deepcopy(functions)
        self.prior_context: Context = prior_context
        self.returned: bool = False

    def find_variable(self, variable_name: str) -> Variable:
        context: Context = self
        while context != None:
            for v in context.variables:
                if variable_name == v.name: 
                    return v 
            context = context.prior_context
        return None

    def find_constant(self, constant_name: str) -> Constant:
        context: Context = self
        while context != None:
            for c in context.constants:
                if constant_name == c.name:
                    return c
            context = context.prior_context
        return None

    def find_function(self, function_name: str) -> Function:
        context: Context = self
        while context != None:
            for f in context.functions + functions:
                if function_name == f.name:
                    return f
            context = context.prior_context
        return None

    def set_variable(self, variable_name: str, value: int | float | str | list) -> None:
        found: Variable = self.find_variable(variable_name)
        found.value = deepcopy(value) # deepcopy je potřeba, můžou proměnné sdílet referenci

    def set_array_element(self, variable_name: str, indices: list[int], value: int | float | str | list) -> None:
        found: Variable = self.find_variable(variable_name)
        self.assign_element(found, indices, value)
    
    def assign_element(self, variable: Variable, indices: list[int], value: int | float | str | list, depth: int = 0, elements: list = []) -> None:
        if depth == 0:
            elements = variable.value
        if depth < len(indices) - 1:
            self.assign_element(variable, indices, value, depth + 1, elements[indices[depth]])
        else:
            elements[indices[depth]] = value