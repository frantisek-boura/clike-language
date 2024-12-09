import sys
from interpreter.program import Program

arguments = sys.argv
code: dict[str, str] = {
    'factorial': '.gramatika_priklady/factorial.txt',
    'dimensions': '.gramatika_priklady/dim_calc.txt',
    'array2d': '.gramatika_priklady/2d_array_sum.txt'
}

if __name__ == '__main__':
    if len(arguments) < 2:
        print(f'No arguments passed, missing filename ({', '.join([f'\"{k}\"' for k in list(code.keys())])})')
        sys.exit()
    if arguments[1] not in list(code.keys()):
        print(f'Invalid filename ({', '.join([f'\"{k}\"' for k in list(code.keys())])})')
        sys.exit()
    input_code: str = code[arguments[1]]
    Program().run(input_code)