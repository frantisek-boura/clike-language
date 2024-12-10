from copy import deepcopy
from typing import Any
from parser import assignable
from parser.array_datatype import ArrayDatatype
from parser.function_parameter import FunctionParameter
from semantics.lib_functions import functions, executables
from interpreter.execution_context import ExecutionContext
from parser.array_declaration import Array
from parser.array_element import ArrayElement
from parser.assign_statement import AssignStatement
from parser.block import Block
from parser.condition import Condition
from parser.constant import Constant
from parser.expressible import Expressible
from parser.expression import Expression
from parser.float_literal import FloatLiteral
from parser.for_statement import ForStatement
from parser.function import Function
from parser.function_call import FunctionCall
from parser.if_statement import IfStatement
from parser.int_literal import IntLiteral
from parser.literal import Literal
from parser.return_statement import ReturnStatement
from parser.statement import Statement
from parser.str_literal import StrLiteral
from parser.variable import Variable

class Interpreter: 
    def __init__(self):
        self.returned_values: list[int | float | str | list] = []
        self.function_context: list[ExecutionContext] = []

    def start(self, block: Block) -> None:
        try:
            self.execute_block(None, block)
        except Exception as e:
            print(e)

    def execute_block(self, context: ExecutionContext, block: Block) -> None:
        new_context: ExecutionContext = ExecutionContext(block.variables, block.constants, block.functions, context)
        for s in block.statements:
            self.execute_statement(new_context, s)
            if len(self.function_context) > 0:
                if self.function_context[-1].returned:
                    break

    def execute_function_block(self, context: ExecutionContext, function: Function, arguments: list) -> None:
        block: Block = function.block
        new_context: ExecutionContext = ExecutionContext(block.variables, block.constants, block.functions, context)
        self.function_context.append(new_context)
        self.evaluate_function_parameters(new_context, function.params, arguments)
        for s in block.statements:
            self.execute_statement(new_context, s)
            if self.function_context[-1].returned:
                break
        self.function_context.pop()

    def execute_statement(self, context: ExecutionContext, statement: Statement) -> None:
        if isinstance(statement, Function):
            return
        elif isinstance(statement, AssignStatement):
            self.execute_assign_statement(context, statement)
        elif isinstance(statement, ForStatement):
            self.execute_for_statement(context, statement)
        elif isinstance(statement, IfStatement):
            self.execute_if_statement(context, statement)
        elif isinstance(statement, ReturnStatement):
            self.execute_return_statement(context, statement)
        elif isinstance(statement, FunctionCall):
            self.execute_function_call(context, statement)

    def execute_for_statement(self, context: ExecutionContext, statement: ForStatement) -> None:
        new_context: ExecutionContext = ExecutionContext([statement.variable], [], [], context)
        self.execute_assign_statement(new_context, statement.starting_assign)
        while self.evaluate_condition(new_context, statement.condition):
            self.execute_block(new_context, statement.block)
            self.execute_assign_statement(new_context, statement.iter_assign)        

    def execute_if_statement(self, context: ExecutionContext, statement: IfStatement) -> None:
        condition: bool = self.evaluate_condition(context, statement.condition)
        if condition:
            self.execute_block(context, statement.block)
            return
        if len(statement.else_ifs) > 0:
            for ei in statement.else_ifs:
                ei: IfStatement = ei
                condition: bool = self.evaluate_condition(context, ei.condition)
                if condition:
                    self.execute_if_statement(context, ei)
                    return
        if statement.else_block != None:
            self.execute_block(context, statement.else_block)

    def evaluate_condition(self, context: ExecutionContext, condition: Condition) -> bool:
        match condition.op:
            case '>':
                return self.evaluate(context, condition.v1) > self.evaluate(context, condition.v2)
            case '<':
                return self.evaluate(context, condition.v1) < self.evaluate(context, condition.v2)
            case '<=':
                return self.evaluate(context, condition.v1) <= self.evaluate(context, condition.v2)
            case '>=':
                return self.evaluate(context, condition.v1) >= self.evaluate(context, condition.v2)
            case '==':
                return self.evaluate(context, condition.v1) == self.evaluate(context, condition.v2)
            case '!=':
                return self.evaluate(context, condition.v1) != self.evaluate(context, condition.v2)

    def evaluate_function_call(self, context: ExecutionContext, statement: FunctionCall) -> int | float | str | list | None:
        self.execute_function_call(context, statement)
        return self.returned_values.pop()

    def execute_function_call(self, context: ExecutionContext, statement: FunctionCall) -> None:
        arguments: list = self.evaluate_function_call_arguments(context, statement.args)
        if statement.name in list(executables.keys()):
            self.execute_lib_function(statement, arguments)
        else:
            function: Function = context.find_function(statement.name)
            self.execute_function_block(context, function, arguments)

    def execute_lib_function(self, statement: FunctionCall, args: list) -> None:
        match statement.name:
            case 'print':
                self.returned_values.append(executables['print'](args[0]))
            case 'read':
                self.returned_values.append(executables['read']())
            case 's_to_i':
                self.returned_values.append(executables['s_to_i'](args[0]))
            case 's_to_f':
                self.returned_values.append(executables['s_to_f'](args[0]))
            case 'i_to_s':
                self.returned_values.append(executables['i_to_s'](args[0]))
            case 'f_to_s':
                self.returned_values.append(executables['f_to_s'](args[0]))
            case 'f_to_i':
                self.returned_values.append(executables['f_to_i'](args[0]))
            case 'i_to_f':
                self.returned_values.append(executables['i_to_f'](args[0]))
            case 'len': 
                self.returned_values.append(executables['len'](args[0]))

    def evaluate_function_parameters(self, context: ExecutionContext, params: list[FunctionParameter], args: list) -> None:
        for i in range(len(params)):
            context.set_variable(params[i].name, args[i])

    def evaluate_function_call_arguments(self, context: ExecutionContext, args: list[Expressible]) -> list:
        new_args: list = []
        for a in args:
            new_args.append(self.evaluate(context, a))
        return new_args

    def execute_return_statement(self, context: ExecutionContext, statement: ReturnStatement) -> None:
        value: int | float | str | list | None = self.evaluate(context, statement.value)
        self.returned_values.append(value)
        self.function_context[-1].returned = True

    def execute_assign_statement(self, context: ExecutionContext, statement: AssignStatement) -> None:
        value: int | float | str | list = self.evaluate(context, statement.value)
        if isinstance(statement.assignable, ArrayElement):
            indices: list[int] = self.evaluate_indices(context, statement.assignable.indices)
            context.set_array_element(statement.assignable.name, indices, value)
        if isinstance(statement.assignable, Variable):
            context.set_variable(statement.assignable.name, value)
    
    def evaluate(self, context: ExecutionContext, value: Expressible | Array) -> int | float | str | list:
        if isinstance(value, (int, float, str, list)):
            return value 
        if isinstance(value, Array):
            return self.evaluate_array(context, value)
        if isinstance(value, Expressible):
            if isinstance(value, Expression):
                return self.evaluate_expression(context, value)
            elif isinstance(value, FunctionCall):
                return self.evaluate_function_call(context, value)
            elif isinstance(value, ArrayElement):
                return self.evaluate_array_element(context, value)
            elif isinstance(value, Variable):
                return self.evaluate_variable(context, value)
            elif isinstance(value, Literal):
                return self.evaluate_literal(value)
    
    def evaluate_array_element(self, context: ExecutionContext, array_element: ArrayElement) -> int | float | str | list:
        variable: Variable = context.find_variable(array_element.name)
        indices: list[int] = self.evaluate_indices(context, array_element.indices)
        return self.access_array_element(variable.value, indices) # variable.value by melo byt uz list, protoze je evaluovan uz pri assign statementu, ktery je nevyhnutelny 
    
    def access_array_element(self, array: list, indices: list[int], depth: int = 0) -> int | float | str | list:
        if depth < len(indices) - 1:
            return self.access_array_element(array[indices[depth]], indices, depth + 1)
        if indices[depth] >= len(array):
            raise Exception(f'Index {indices[depth]} out of bounds ({len(array)})')
        return array[indices[depth]]

    def evaluate_literal(self, value: Literal) -> int | float | str:
        if isinstance(value, IntLiteral):
            return int(value.value)
        if isinstance(value, FloatLiteral):
            return float(value.value)
        if isinstance(value, StrLiteral):
            return str(value.value)

    def evaluate_variable(self, context: ExecutionContext, variable: Variable) -> int | float | str | list:
        var: Variable = context.find_variable(variable.name)
        if var == None:
            const: Constant = context.find_constant(variable.name)
            return self.evaluate(context, const.value)
        else:
            return var.value

    def evaluate_expression(self, context: ExecutionContext, expression: Expression) -> int | float | str :
        if expression.datatype.name == 'str': 
            return self.evaluate_str(context, expression)
        result: float | int = 0
        term_result: float = 0.0
        for t in expression.terms:
            factor_result: float = 0.0
            for f in t.factors:
                value: int | float = self.evaluate(context, f.value)
                if type(value) == list:
                    return value 
                if f.op == None:
                    factor_result = value
                    continue
                match f.op:
                    case '*':
                        if expression.datatype.name == 'int':
                            factor_result = int(factor_result * value)
                        else:    
                            factor_result = float(factor_result * value)
                    case '/':
                        if value == 0:
                            raise Exception('Division by 0')
                        if expression.datatype.name == 'int':
                            factor_result = int(factor_result / value)
                        else:    
                            factor_result = float(factor_result / value)
            match t.op:
                case '+':
                    if expression.datatype.name == 'int':
                        term_result = int(term_result + factor_result)
                    else:    
                        term_result = float(term_result + factor_result)
                case '-':
                    if expression.datatype.name == 'int':
                        term_result = int(term_result - factor_result)
                    else:    
                        term_result = float(term_result - factor_result)
        match expression.op:
            case '+':
                if expression.datatype.name == 'int':
                    result = int(+term_result)
                else:
                    result = float(+term_result)
            case '-':
                if expression.datatype.name == 'int':
                    result = int(-term_result)
                else:
                    result = float(-term_result)
        return result

    def evaluate_str(self, context: ExecutionContext, expression: Expression) -> str:
        result: str = ''
        for t in expression.terms:
            for f in t.factors:
                value: str = self.evaluate(context, f.value)
                result += value
        return result
    
    def evaluate_array(self, context: ExecutionContext, value: Array | list) -> list:
        if isinstance(value, Array):
            return self.evaluate_array(context, value.elements)
        if isinstance(value, list):
            return [self.evaluate_array(context, x) for x in value]
        return self.evaluate(context, value)
            
    def evaluate_indices(self, context: ExecutionContext, indices: list[Expressible]) -> list[int]:
        new_indices: list[int] = []
        for i in indices:
            index: int = self.evaluate(context, i)
            new_indices.append(index)
        return new_indices