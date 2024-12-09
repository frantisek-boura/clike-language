#from functools import reduce

#sizes: list[int] = [2, 3, 1]
#elements_count: int = reduce(lambda a, b: a * b, sizes)
#indices: list[int] = [0 for _ in range(len(sizes))]
#for el in range(elements_count):
    #print(f'variable@{'_'.join([str(x) for x in indices])}')
    #indices[len(sizes) - 1] += 1
    #for i in range(len(indices)):
        #if indices[len(sizes) - 1 - i] >= sizes[len(sizes) - 1 - i]:
            #indices[len(sizes) - 1 - i] = 0
            #indices[len(sizes) - 2 - i] += 1
    

#sizes = [1, 2, 3]
#indices = [0, 1]
#diff = len(sizes) - len(indices)
#print(sizes[len(sizes) - diff:])

from file import read_file
from interpreter.execution_context import ExecutionContext
from interpreter.interpreter import Interpreter
from interpreter.program import Program
from parser.block import Block
from parser.variable import Variable
from semantics.semantics import Semantics
from tokens.tokiter import PeekableIter
from tokens.tokenizer import get_tokens
from parser.ast import AST

code = read_file('.gramatika_priklady/test.txt')
iter = get_tokens(code)
ast: AST = AST(PeekableIter(iter))
block: Block = ast.parse()
semantics: Semantics = Semantics()
result: bool = semantics.validate(block)
print(block)
print(result)
if (result):
    interpreter: Interpreter = Interpreter()
    interpreter.start(block)

