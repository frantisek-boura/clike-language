import traceback
from parser.array_datatype import ArrayDatatype
from parser.array_declaration import Array 
from parser.array_element import ArrayElement
from parser.assign_statement import AssignStatement
from parser.assignable import Assignable
from parser.condition import Condition
from parser.datatype import Datatype
from parser.expressible import Expressible
from parser.expression import Expression
from parser.factor import Factor
from parser.float_literal import FloatLiteral
from parser.for_statement import ForStatement
from parser.function_call import FunctionCall
from parser.if_statement import IfStatement
from parser.int_literal import IntLiteral
from parser.literal import Literal
from parser.return_statement import ReturnStatement
from parser.statement import Statement
from parser.str_literal import StrLiteral
from parser.term import Term
from semantics.lib_functions import functions
from parser.ast import AST
from parser.block import Block
from parser.constant import Constant
from parser.function import Function
from parser.variable import Variable

class Semantics:
    def __init__(self):
        self.var_stack: list[Variable] = []
        self.const_stack: list[Constant] = []
        self.func_stack: list[Function] = []
        self.currently_in: Function = None 
    
    def find_var(self, name: str) -> Variable:
        for v in self.var_stack:
            if v.name == name:
                return v
        return None
    
    def find_const(self, name: str) -> Constant:
        for c in self.const_stack:
            if c.name == name:
                return c
        return None

    def find_func(self, name: str) -> Function:
        for f in self.func_stack + functions:
            if f.name == name:
                return f
        return None

    def validate(self, block: Block) -> bool:
        try:
            self.check_block(block)
            return True
        except Exception as e:
            print(e)
            return False 

    def check_block(self, block: Block) -> None:
        for v in block.variables:
            if self.find_var(v.name) != None:
                raise Exception(f'Variable with name {v.name} already defined')
            self.var_stack.append(v)
        for c in block.constants:
            if self.find_const(c.name) != None:
                raise Exception(f'Constant with name {c.name} already defined')
            self.const_stack.append(c)
        for f in block.functions:
            if self.find_func(f.name) != None:
                raise Exception(f'Function with name {f.name} already defined')
            self.func_stack.append(f)
        for s in block.statements:
            self.check_statement(s)
        for v in block.variables:
            self.var_stack.remove(v)
        for c in block.constants:
            self.const_stack.remove(c)
        for f in block.functions:
            self.func_stack.remove(f)
    
    def check_statement(self, statement: Statement) -> None:
        if isinstance(statement, AssignStatement):
            self.check_assign_statement(statement)
        if isinstance(statement, FunctionCall):
            self.check_function_call(statement)
        if isinstance(statement, Function):
            self.check_function(statement)
        if isinstance(statement, ReturnStatement):
            self.check_return_statement(statement)
        if isinstance(statement, IfStatement):
            self.check_if_statement(statement)
        if isinstance(statement, ForStatement):
            self.check_for_statement(statement)

    def check_for_statement(self, statement: ForStatement) -> None:
        if self.find_var(statement.variable.name) != None:
            raise Exception(f'Variable with name {statement.variable.name} already defined')
        self.var_stack.append(statement.variable)
        self.check_assign_statement(statement.starting_assign)
        self.check_condition(statement.condition)
        self.check_assign_statement(statement.iter_assign)
        self.check_block(statement.block)
        self.var_stack.remove(statement.variable)

    def check_if_statement(self, statement: IfStatement) -> None:
        self.check_condition(statement.condition)
        self.check_block(statement.block)
        for i in statement.else_ifs:
            self.check_if_statement(i)
        if statement.else_block != None:
            self.check_block(statement.else_block)
    
    def check_condition(self, condition: Condition) -> None:
        dt1: Datatype = self.check_expression(condition.v1)
        dt2: Datatype = self.check_expression(condition.v2)
        self.compare_datatypes(dt1, dt2)
        if dt1.name == str and condition.op not in ('==', '!='):
            raise Exception(f'Cannot compare strings with op {condition.op}')

    def check_return_statement(self, statement: ReturnStatement) -> None:
        if self.currently_in == None:
            raise Exception('Random return statement')
        if statement.value == None:
            return
        if isinstance(statement.value, Array):
            self.compare_datatypes(self.currently_in.datatype, statement.value.datatype)
        elif isinstance(statement.value, Expression):
            datatype: Datatype = self.check_expression(statement.value)
            self.compare_datatypes(self.currently_in.datatype, datatype)
            statement.value.datatype = datatype

    def check_function(self, statement: Function) -> None:
        self.currently_in = statement
        datatype: Datatype = statement.datatype
        if datatype.name != 'void':
            block: Block = statement.block
            found: bool = False
            for s in block.statements:
                if isinstance(s, ReturnStatement):
                    found: bool = True
                    break
            if not found:
                raise Exception(f'Missing return statement in function {statement.name}')
        self.check_block(statement.block)
        self.currently_in = None 
    
    def check_function_call(self, statement: FunctionCall) -> Datatype:
        existing_function: Function = self.find_func(statement.name)
        if existing_function == None:
            raise Exception(f'Function with name {statement.name} not defined')
        statement.datatype = existing_function.datatype
        existing_param_count: int = len(existing_function.params)
        call_param_count: int = len(statement.args)
        if existing_param_count != call_param_count:
            raise Exception(f'Function {statement.name} requires {existing_param_count} parameters, {call_param_count} provided')
        for i in range(len(existing_function.params)):
            param_datatype: Datatype = existing_function.params[i].datatype
            call_arg_datatype: Datatype = self.check_expression(statement.args[i])
            self.compare_datatypes(param_datatype, call_arg_datatype)
        return existing_function.datatype

    def check_assign_statement(self, statement: AssignStatement) -> None:
        assignable: Variable | ArrayElement = statement.assignable
        existing_variable: Variable = self.find_var(assignable.name)
        if existing_variable == None:
            raise Exception(f'Variable with name {assignable.name} not defined')
        if isinstance(statement.assignable, ArrayElement) and isinstance(statement.value, Array):
            self.check_array(statement.value)
            statement.assignable.datatype = self.find_array_element_datatype(statement.assignable, existing_variable)
            value_datatype: ArrayDatatype = statement.value.datatype
            statement.value.datatype = value_datatype
            self.compare_datatypes(statement.assignable.datatype, value_datatype)
        elif isinstance(statement.assignable, ArrayElement) and isinstance(statement.value, Expression):
            statement.assignable.datatype = self.find_array_element_datatype(statement.assignable, existing_variable)
            value_datatype: Datatype = self.check_expression(statement.value)
            if statement.assignable.datatype.name == 'float' and value_datatype.name == 'int':
                value_datatype.name = 'float'
            elif statement.assignable.datatype.name == 'int' and value_datatype.name == 'float':
                value_datatype.name = 'int'
            statement.value.datatype = value_datatype
            self.compare_datatypes(statement.assignable.datatype, value_datatype)
        elif isinstance(statement.assignable, Variable) and isinstance(statement.value, Array):
            self.check_array(statement.value)
            statement.assignable.datatype = existing_variable.datatype
            value_datatype: ArrayDatatype = statement.value.datatype
            statement.value.datatype = value_datatype
            self.compare_datatypes(statement.assignable.datatype, value_datatype)
        elif isinstance(statement.assignable, Variable) and isinstance(statement.value, Expression):
            statement.assignable.datatype = existing_variable.datatype
            value_datatype: Datatype = self.check_expression(statement.value)
            if statement.assignable.datatype.name == 'float' and value_datatype.name == 'int':
                value_datatype.name = 'float'
            elif statement.assignable.datatype.name == 'int' and value_datatype.name == 'float':
                value_datatype.name = 'int'
            statement.value.datatype = value_datatype
            self.compare_datatypes(statement.assignable.datatype, value_datatype)
        else:
            raise Exception('Invalid assign statement')

    def check_expression(self, expression: Expression) -> Datatype:
        expression_op: str = expression.op
        term_datatype: Datatype = None
        term_first_iter: bool = True
        for term in expression.terms:
            temp_term_dt: Datatype = None
            term_op: str = term.op
            factor_datatype: Datatype = None
            factor_first_iter: bool = True
            for factor in term.factors:
                temp_factor_dt: Datatype = None
                factor_op: str = factor.op
                value: Variable | ArrayElement | Constant | Literal | FunctionCall | Expression = factor.value 
                if isinstance(value, Variable):
                    variable: Variable = self.find_var(value.name)
                    if variable == None:
                        constant: Constant = self.find_const(value.name)
                        if constant == None:
                            raise Exception(f'No variable or constant with name {value.name} defined')
                        temp_factor_dt: Datatype = constant.datatype
                        value.datatype = constant.datatype
                    else:
                        temp_factor_dt: Datatype = variable.datatype
                        value.datatype = variable.datatype
                elif isinstance(value, ArrayElement):
                    variable: Variable = self.find_var(value.name)
                    if variable == None:
                        raise Exception(f'Variable with name {value.name} is not defined')
                    datatype: Datatype = self.find_array_element_datatype(value, variable)
                    value.datatype = datatype
                    temp_factor_dt: Datatype = datatype
                elif isinstance(value, Literal):
                    if isinstance(value, IntLiteral):
                        temp_factor_dt = Datatype('int')
                    elif isinstance(value, FloatLiteral):
                        temp_factor_dt = Datatype('float')
                    elif isinstance(value, StrLiteral):
                        temp_factor_dt = Datatype('str')
                elif isinstance(value, FunctionCall):
                    datatype: Datatype = self.check_function_call(value)
                    value.datatype = datatype
                    temp_factor_dt: Datatype = datatype
                elif isinstance(value, Expression):
                    datatype: Datatype = self.check_expression(value)
                    value.datatype = datatype
                    temp_factor_dt: Datatype = datatype
                if factor_first_iter:
                    factor_datatype = temp_factor_dt
                    factor_first_iter = False
                else:
                    factor_datatype = self.check_expression_operation_datatype(factor_datatype, factor_op, temp_factor_dt)
                temp_term_dt = factor_datatype
            if term_first_iter:
                term_datatype = temp_term_dt
                term_first_iter = False
            else:
                term_datatype = self.check_expression_operation_datatype(term_datatype, term_op, temp_term_dt)
        if term_datatype.name == 'str':
            if expression_op != '+':
                raise Exception(f'Invalid operator, cannot perform {expression_op} on strings')
        expression.datatype = term_datatype
        return term_datatype

    def check_expression_operation_datatype(self, dt1: Datatype, op: str, dt2: Datatype) -> Datatype:
        if 'float' in (dt1.name, dt2.name) and 'int' in (dt1.name, dt2.name) and op in '+-*/':
            return Datatype('float')
        self.compare_datatypes(dt1, dt2)
        if dt1.name == 'int': # V tuhle chvíli není možné, aby dt2 byl jiný datový typ
            if op in '+-*/':
                return Datatype('int')
        elif dt1.name == 'float':
            if op in '+-*/':
                return Datatype('float')
        elif dt1.name == 'str':
            if op == '+':
                return Datatype('str')
        raise Exception(f'Invalid operation, cannot perform {dt1} {op} {dt2}')

    def check_array(self, array: Array, depth: int = 1, elements: list = None) -> None:
        dimensions: int = array.datatype.dimensions - depth
        if dimensions < 0:
            print(dimensions)
            raise Exception(f'Invalid array depth, array is too deep for datatype {array.datatype}')
        if dimensions > 0:
            element_datatype: ArrayDatatype = ArrayDatatype(array.datatype.name, dimensions)
        else:
            element_datatype: Datatype = Datatype(array.datatype.name)
        if elements == None:
            elements = array.elements
        for el in elements:
            if type(el) == list:
                self.check_array(array, depth + 1, el)
            else:
                expression: Expression = el
                datatype: Datatype = self.check_expression(expression)
                self.compare_datatypes(element_datatype, datatype)
                expression.datatype = datatype

    def check_array_element_indices(self, array_element: ArrayElement) -> None:
        for i in array_element.indices:
            datatype: Datatype = self.check_expression(i)
            if datatype.name != 'int':
                raise Exception(f'Invalid index datatype, cannot index with type {datatype.name}')

    def find_array_element_datatype(self, array_element: ArrayElement, existing_variable: Variable) -> Datatype:
        indices_count: int = len(array_element.indices)
        if type(existing_variable.datatype) != ArrayDatatype:
            raise Exception(f'Variable with name {existing_variable.name} is not an array')
        existing_datatype: ArrayDatatype = existing_variable.datatype
        if indices_count > existing_datatype.dimensions:
            raise Exception(f'Array with name {existing_variable.name} has only {existing_datatype.dimensions} dimensions, {indices_count} addressed')
        self.check_array_element_indices(array_element)
        dimensions: int = existing_datatype.dimensions - indices_count
        if dimensions == 0:
            datatype: Datatype = Datatype(existing_datatype.name)
        else:
            datatype: Datatype = ArrayDatatype(existing_datatype.name, dimensions)
        array_element.datatype = datatype
        return datatype
        
    def compare_datatypes(self, dt1: Datatype | ArrayDatatype, dt2: Datatype | ArrayDatatype) -> None:
        valid: bool = False 
        if dt1.name == 'any':
            return True
        if dt1.name == 'array':
            if type(dt1) != type(dt2) or dt1.dimensions != dt2.dimensions or type(dt1) != ArrayDatatype or type(dt2) != ArrayDatatype:
                return False
            return True
        if type(dt1) == Datatype:
            if type(dt1) == type(dt2):
                valid = dt1.name == dt2.name
            else:
                valid = False
        elif type(dt1) == ArrayDatatype:
            if type(dt1) == type(dt2): 
                valid = dt1.name == dt2.name and dt1.dimensions == dt2.dimensions
            else:
                valid = False
        else:
            valid = False
        if not valid:
            raise Exception(f'Incompatible datatypes {dt1} and {dt2}')
        

    
    
        
        









        





         







