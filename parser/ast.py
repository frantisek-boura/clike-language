from functools import reduce
from typing import Any, List, Tuple
from parser.array_datatype import ArrayDatatype
from parser.array_declaration import Array
from parser.array_element import ArrayElement
from parser.assign_statement import AssignStatement
from parser.assignable import Assignable
from parser.block import Block
from parser.condition import Condition
from parser.constant import Constant
from parser.datatype import Datatype
from parser.expressible import Expressible
from parser.expression import Expression
from parser.factor import Factor
from parser.float_literal import FloatLiteral
from parser.for_statement import ForStatement
from parser.function import Function
from parser.function_call import FunctionCall
from parser.function_parameter import FunctionParameter
from parser.if_statement import IfStatement
from parser.int_literal import IntLiteral
from parser.literal import Literal
from parser.return_statement import ReturnStatement
from parser.statement import Statement
from parser.str_literal import StrLiteral
from parser.term import Term
from parser.variable import Variable
from tokens.tokiter import PeekableIter

class AST:
    def __init__(self, iter: PeekableIter):
        self.iter: PeekableIter = iter

    def variable_exists(self, name: str, variables: list[Variable]) -> bool:
        for v in variables:
            if name == v.name:
                return True
        return False
    
    def parse(self) -> Block:
        try:
            return self.read_block()
        except Exception as e:
            print(e)

    def read_block(self) -> Block:
        block: Block = Block()
        result: Any = None
        if self.iter.peek().type == '{':
            self.iter.next() # Skip {
        while self.iter.peek() != None:
            result: Any = self.read_statement()
            if result != None:
                self.eval_result(result, block)
            if self.iter.peek() == None:
                break
            if self.iter.peek().type == ';':
                self.iter.next() # Skip ;
                continue
            elif self.iter.peek() == None:
                break # Konec souboru
            elif self.iter.peek().type == '}':
                self.iter.next() # Skip }
                break # Konec bloku
        return block

    def eval_result(self, result: Any, block: Block) -> None:
        if isinstance(result, Function):
            function: Function = result
            block.functions.append(function) 
            block.statements.append(function)
        elif isinstance(result, Constant):
            block.constants.append(result)
        elif isinstance(result, FunctionCall):
            block.statements.append(result)
        elif isinstance(result, AssignStatement):
            block.statements.append(result)
        elif isinstance(result, tuple) and isinstance(result[0], Variable) and isinstance(result[1], AssignStatement):
            variable: Variable = result[0]
            assign_statement: AssignStatement = result[1]
            block.variables.append(variable)
            block.statements.append(assign_statement)
        elif isinstance(result, Variable):
            block.variables.append(result)
        elif isinstance(result, ForStatement):
            block.statements.append(result)
        elif isinstance(result, IfStatement):
            block.statements.append(result)
        elif isinstance(result, ReturnStatement):
            block.statements.append(result)
        else:
            raise Exception('Unexpected statement')

    def read_statement(self) -> Any:
        if self.iter.peek() == None:
            return None # Konec souboru
        if self.iter.peek().type == 'const': # Constant declaration
            return self.read_constant_declaration()
        if self.iter.peek().type in ('int', 'float', 'str', 'void'): # Variable/Function declaration
            return self.read_declaration()
        if self.iter.peek().type == 'name': # Function Call, Assignment (Variable, ArrayElement)
            return self.read_named_statement()
        if self.iter.peek().type == 'for': # For statement
            return self.read_for_statement()
        if self.iter.peek().type == 'if': # If statement
            return self.read_if_statement()
        if self.iter.peek().type == 'return': # Return statement
            return self.read_return_statement()
        if self.iter.peek().type == '}':
            return None # Konec bloku

    def read_for_statement(self) -> ForStatement:
        for_statement: ForStatement = ForStatement()
        self.iter.next() # Skip for
        if self.iter.peek().type != '(':
            raise Exception('Unexpected token, expected (')
        self.iter.next() # Skip (
        if self.iter.peek().type in ('int', 'float', 'str'):
            control_variable: Tuple[Variable, AssignStatement] = self.read_declaration()
            if isinstance(control_variable, Variable):
                raise Exception('Unexpected statement, uninitialized loop control variable')
            for_statement.variable = control_variable[0]
            for_statement.starting_assign = control_variable[1]
        else:
            raise Exception('Unexpected token, expected datatype')
        if self.iter.peek().type != ';':
            raise Exception('Unexpected token, expected ,')
        self.iter.next() # Skip ,
        condition: Condition = self.read_condition()
        for_statement.condition = condition
        if self.iter.peek().type != ';':
            raise Exception('Unexpected token, expected ,')
        self.iter.next() # Skip ,
        if self.iter.peek().type != 'name':
            raise Exception('Unexpected token, expected name')
        iter_assign: AssignStatement = self.read_named_statement()
        if isinstance(iter_assign, FunctionCall):
            raise Exception('Unexpected statement, expected assign statement')
        for_statement.iter_assign = iter_assign
        if self.iter.peek().type != ')':
            raise Exception('Unexpected token, expected )')
        self.iter.next() # Skip )
        if self.iter.peek().type != '{':
            raise Exception('Unexpected token, expected {')
        block: Block = self.read_block()
        for_statement.block = block
        return for_statement

    def read_if_statement(self, branch: bool = False) -> IfStatement:
        if_statement: IfStatement = IfStatement()
        self.iter.next() # Skip if
        if self.iter.peek().type != '(':
            raise Exception('Unexpected token, expected (')
        self.iter.next() # Skip (
        condition = self.read_condition()
        if_statement.condition = condition
        if self.iter.peek().type != ')':
            raise Exception('Unexpected token, expected )')
        self.iter.next() # Skip )
        if self.iter.peek().type != '{':
            raise Exception('Unexpected token, expected {')
        block: Block = self.read_block()
        if_statement.block = block
        if branch:
            return if_statement
        else_ifs: list[IfStatement] = []
        if self.iter.peek() == None:
            return if_statement
        while self.iter.peek().type == 'else':
            self.iter.next() # Skip else
            if self.iter.peek().type == 'if':
                else_if_statement: IfStatement = self.read_if_statement(True)
                else_ifs.append(else_if_statement)
            elif self.iter.peek().type == '{':
                else_block: Block = self.read_block()
                if_statement.else_block = else_block
                break
            else:
                raise Exception('Unexpected token, expected if or {')
        if_statement.else_ifs = else_ifs
        return if_statement

    def read_return_statement(self) -> ReturnStatement:
        self.iter.next() # Skip return
        return_statement: ReturnStatement = ReturnStatement(None)
        if self.iter.peek().type in ('+', '-', '(', 'name', 'lit_int', 'lit_float', 'lit_str'):
            value: Expressible = self.read_expression()
        else:
            value: Array = self.read_array('return')
        return_statement.value = value 
        return return_statement
        
    def read_condition(self) -> Condition:
        v1: Expressible = self.read_expression()
        if self.iter.peek().type not in ('<', '>', '<=', '>=', '==', '!='):
            raise Exception('Unexpected token, expected compare operator')
        op: str = self.iter.next().value
        v2: Expressible = self.read_expression()
        condition: Condition = Condition(v1, op, v2)
        return condition

    def read_named_statement(self) -> FunctionCall | AssignStatement:
        name: str = self.iter.next().value
        if self.iter.peek().type == '(':
            function_call: FunctionCall = self.read_function_call(name)
            return function_call
        assignable: Assignable
        if self.iter.peek().type == '[':
            assignable: ArrayElement = self.read_array_element(name)
        else:
            # Zde se předává jako datový typ None, protože ho zjistí až sémantická analýza
            assignable: Variable = Variable(name, None)
        if self.iter.peek().type != '=':
            raise Exception('Unexpected token, expected =')
        self.iter.next() # Skip =
        if self.iter.peek().type in ('int', 'float', 'str'):
            value: Array = self.read_array()
        else:
            value: Expressible = self.read_expression()
        assign_statement: AssignStatement = AssignStatement(assignable, value)
        return assign_statement

    def read_array_element(self, name: str) -> ArrayElement:
        indices: list[Expressible] = []
        while True:
            if self.iter.peek().type != '[':
                break
            self.iter.next() # Skip [
            expression: Expressible = self.read_expression()
            indices.append(expression)
            if self.iter.peek().type != ']':
                raise Exception('Unexpected token, expected ]')
            self.iter.next() # Skip ]
        # Zde se předává jako datový typ None, protože ho zjistí až sémantická analýza
        return ArrayElement(name, None, indices)

    def read_literal(self) -> Literal:
        value: Literal = None
        match self.iter.peek().type:
            case 'lit_int':
                value: IntLiteral = IntLiteral(int(self.iter.next().value))
            case 'lit_float':
                value: FloatLiteral = FloatLiteral(float(self.iter.next().value))
            case 'lit_str':
                value: StrLiteral = StrLiteral(self.iter.next().value)
        return value

    def read_constant_declaration(self) -> Constant:
        self.iter.next() # Skip const
        if self.iter.peek().type not in ('int', 'float', 'str'):
            raise Exception('Unexpected token, expected datatype')
        datatype: Datatype = Datatype(self.iter.next().value)
        if self.iter.peek().type != 'name':
            raise Exception('Unexpected token, expected name')
        name: str = self.iter.next().value
        if self.iter.peek().type != '=':
            raise Exception('Unexpected token, expected assign symbol \'=\'')
        self.iter.next() 
        if self.iter.peek().type not in ('lit_int', 'lit_float', 'lit_str'):
            raise Exception('Unexpected token, expected literal')
        value: Literal = self.read_literal()
        constant: Constant = Constant(name, datatype, value)
        return constant

    def read_declaration(self) -> Function | Tuple[Variable, AssignStatement] | Variable:
        datatype: Datatype = Datatype(self.iter.next().value)
        dimensions: int = self.read_dimensions()
        if dimensions > 0:
            datatype: ArrayDatatype = ArrayDatatype(datatype.name, dimensions)
        if self.iter.peek().type != 'name':
            raise Exception('Unexpected token, expected name')
        name: str = self.iter.next().value
        if self.iter.peek().type == '(':
            function: Function = self.read_function_declaration(name, datatype)
            return function
        if self.iter.peek().type == '=':
            self.iter.next() # Skip =
            variable: Variable = Variable(name, datatype)
            if self.iter.peek().type in ('int', 'float', 'str'):
                expression: Array = self.read_array()
            else:
                expression: Expressible = self.read_expression()
            assign_statement: AssignStatement = AssignStatement(variable, expression)
            return (variable, assign_statement)
        variable: Variable = Variable(name, datatype)
        return variable
    
    def read_expression(self) -> Expressible:
        op: str = '+'
        if self.iter.peek().type in '+-':
            op: str = self.iter.next().value
        terms: list[Term] = []
        while True:
            terms.append(self.read_term())
            if not self.iter.peek().type in ('+', '-', 'name', 'lit_int', 'lit_float', 'lit_str', '('):
                break
        expression: Expression = Expression(op, terms)
        return expression

    def read_term(self) -> Term:
        op: str = '+'
        if self.iter.peek().type in '+-':
            op: str = self.iter.next().value
        factors: list[Factor] = []
        while True:
            factors.append(self.read_factor())
            if not self.iter.peek().type in ('*', '/', 'name', 'lit_int', 'lit_float', 'lit_str', '('):
                break
        term: Term = Term(op, factors)
        return term

    def read_factor(self) -> Factor: 
        # Literal, Function Call, Array Element, Variable, Array
        # None v defaultu, protože první člen nemůže mít matematický operátor
        # jelikož např. "*10" sám o sobě není validní výraz
        op: str = None 
        if self.iter.peek().type in '*/':
            op: str = self.iter.next().value
        value: Expressible 
        if self.iter.peek().type in ('lit_int', 'lit_float', 'lit_str'):
            value: Literal = self.read_literal()
        elif self.iter.peek().type == 'name':
            name: str = self.iter.next().value
            if self.iter.peek().type == '(':
                value: FunctionCall = self.read_function_call(name)
            elif self.iter.peek().type == '[':
                value: ArrayElement = self.read_array_element(name)
            else:
                # Zde se předává jako datový typ None, protože ho zjistí až sémantická analýza
                value: Variable = Variable(name, None)
        elif self.iter.peek().type == '(':
            self.iter.next() # Skip (
            value: Expression = self.read_expression()
            if self.iter.peek().type != ')':
                raise Exception('Unexpected token, expected )')
            self.iter.next() # Skip )
        factor: Factor = Factor(op, value)
        return factor

    def read_function_call(self, name: str) -> FunctionCall:
        args: list[Expressible] = self.read_arguments()
        # Zde se předává jako datový typ None, protože ho zjistí až sémantická analýza
        function_call: FunctionCall = FunctionCall(name, None, args)
        return function_call

    def read_arguments(self) -> list[Expressible]:
        args: list[Expressible] = []
        self.iter.next() # Skip (
        while self.iter.peek().type != ')':
            if self.iter.peek().type not in ('+', '-', '(', 'name', 'lit_int', 'lit_float', 'lit_str'):
                raise Exception('Unexpected token, expected expression')
            expression: Expressible = self.read_expression()
            args.append(expression)
            if self.iter.peek().type == ')':
                break
            if self.iter.peek().type != ',':
                raise Exception('Unexpected token, expected ,')
            self.iter.next() # Skip ,
        self.iter.next() # Skip )
        return args

    def read_function_declaration(self, name: str, datatype: Datatype) -> Function:
        params: list[FunctionParameter] = self.read_function_parameters()
        if self.iter.peek().type != '{':
            raise Exception('Unexpected token, expected {')
        block: Block = self.read_block()
        for p in params:
            parameter_variable: Variable = Variable(p.name, p.datatype)
            block.variables.append(parameter_variable)
        function: Function = Function(name, datatype, params, block)
        return function

    def read_function_parameters(self) -> List[FunctionParameter]:
        self.iter.next() # Skip (
        params: list[FunctionParameter] = []
        while True:
            if self.iter.peek().type in ('int', 'float', 'str'):
                datatype: Datatype = Datatype(self.iter.next().value)
                dimensions: int = self.read_dimensions()
                if dimensions > 0:
                    datatype: ArrayDatatype = ArrayDatatype(datatype.name, dimensions)
                if self.iter.peek().type != 'name':
                    raise Exception('Unexpected token, expected name')
                name: str = self.iter.next().value
                param: FunctionParameter = FunctionParameter(name, datatype)
                params.append(param)
                if self.iter.peek().type == ',':
                    self.iter.next() # Skip ,
                    continue
            elif self.iter.peek().type == ')':
                self.iter.next() # Skip )
                break
            else:
                raise Exception('Unexpected token') 
        return params

    def read_dimensions(self) -> int:
        dimensions: int = 0
        while self.iter.peek().type == '[':
            self.iter.next() # Skip [
            if self.iter.peek().type != ']':
                raise Exception('Invalid array datatype, missing closing bracket')
            self.iter.next() # Skip ]
            dimensions += 1
        return dimensions
    
    def read_dimensions_and_sizes(self) -> Tuple[str, int, list[int]]:
        datatype_name: str = self.iter.next().value
        dimensions: int = 0
        sizes: list[int] = []
        while True:
            if self.iter.peek().type == '@' or self.iter.peek().type == ';':
                break
            self.iter.next() # Skip [
            if self.iter.peek().type != 'lit_int':
                raise Exception('Unexpected token, expected int literal')
            sizes.append(int(self.iter.next().value))
            dimensions += 1
            if self.iter.peek().type != ']':
                raise Exception('Unexpected token, expected ]')
            self.iter.next() # Skip ]
        return (datatype_name, dimensions, sizes)

    def read_array(self) -> Array:
        (datatype_name, dimensions, sizes) = self.read_dimensions_and_sizes()
        datatype: ArrayDatatype = ArrayDatatype(datatype_name, dimensions)
        if self.iter.peek().type == ';':
            default_value: Expressible = None
            match datatype.name:
                case 'int':
                    default_value: Expression = Expression('+', [Term('+', [Factor(None, IntLiteral(0))])])
                case 'float':
                    default_value: Expression = Expression('+', [Term('+', [Factor(None, FloatLiteral(0.0))])])
                case 'str':
                    default_value: Expression = Expression('+', [Term('+', [Factor(None, StrLiteral(''))])])
            elements: list = self.preallocate_array(sizes, default_value)
        elif self.iter.peek().type == '@':
            self.iter.next() # Skip @
            elements: list = self.read_array_elements(sizes)
        array: Array = Array(elements, datatype)
        return array

    def preallocate_array(self, sizes: list[int], value: Expression, depth: int = 0) -> list:
        els: list = []
        for _ in range(sizes[depth]):
            if depth < len(sizes) - 1:
                els.append(self.preallocate_array(sizes, value, depth + 1))
                continue
            els.append(value)
        return els

    def read_array_elements(self, sizes: list[int], depth: int = 0) -> list:
        if self.iter.peek().type != '[':
            raise Exception('Unexpected token, expected [')
        self.iter.next() # Skip [
        els: list = []
        for _ in range(sizes[depth]):
            if depth < len(sizes) - 1:
                els.append(self.read_array_elements(sizes, depth + 1))
                if self.iter.peek().type == ']':
                    break
                if self.iter.peek().type != ',':
                    raise Exception('Unexpected token, expected ,')
                self.iter.next() # Skip ,
                continue
            expression: Expressible = self.read_expression()
            els.append(expression)
            if self.iter.peek().type == ',': 
                self.iter.next() # Skip ,
                continue
        if self.iter.peek().type != ']':
            raise Exception('Unexpected token, expected ]')
        self.iter.next() # Skip ]
        return els



