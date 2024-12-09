from interpreter.execution_context import ExecutionContext
from interpreter.interpreter import Interpreter
from parser.ast import AST
from parser.block import Block
from semantics.semantics import Semantics
from tokens.tokiter import PeekableIter
from tokens.tokenizer import get_tokens
from file import read_file

class Program:
    def run(self, input_code: str):
        code = read_file(input_code)
        tokens = get_tokens(code)
        iter: PeekableIter = PeekableIter(tokens)
        ast: Block = AST(iter).parse()
        valid: bool = Semantics().validate(ast)
        if valid:
            Interpreter().start(ast)