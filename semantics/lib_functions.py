from parser.array_datatype import ArrayDatatype
from parser.array_declaration import Array
from parser.datatype import Datatype
from parser.function import Function
from parser.function_parameter import FunctionParameter

functions: list[Function] = [
    # Funkce pro uživatelský input z terminálu
    Function(
        'read',                                             # Název funkce
        Datatype('str'),                                    # Návratový typ
        [],                                                 # Parametry funkce
        None # Nepotřebuji definovat body pro tyto funkce, řeším je v interpretu
    ),
    Function(
        'print',                                            # Název funkce
        Datatype('void'),                                   # Návratový typ
        [
            FunctionParameter('text', Datatype('str'))      # Parametry funkce
        ],     
        None # Nepotřebuji definovat body pro tyto funkce, řeším je v interpretu
    ),
    Function(
        's_to_i',                                           # Název funkce
        Datatype('int'),                                    # Návratový typ
        [
            FunctionParameter('text', Datatype('str'))      # Parametry funkce
        ],     
        None # Nepotřebuji definovat body pro tyto funkce, řeším je v interpretu
    ),
    Function(
        's_to_f',                                           # Název funkce
        Datatype('float'),                                  # Návratový typ
        [
            FunctionParameter('text', Datatype('str'))      # Parametry funkce
        ],     
        None # Nepotřebuji definovat body pro tyto funkce, řeším je v interpretu
    ),
    Function(
        'i_to_s',                                           # Název funkce
        Datatype('str'),                                    # Návratový typ
        [
            FunctionParameter('value', Datatype('int'))     # Parametry funkce
        ],     
        None # Nepotřebuji definovat body pro tyto funkce, řeším je v interpretu
    ),
    Function(
        'f_to_s',                                           # Název funkce
        Datatype('str'),                                    # Návratový typ
        [
            FunctionParameter('value', Datatype('float'))   # Parametry funkce
        ],     
        None # Nepotřebuji definovat body pro tyto funkce, řeším je v interpretu
    ),
    Function(
        'f_to_i',                                           # Název funkce
        Datatype('int'),                                    # Návratový typ
        [
            FunctionParameter('value', Datatype('float'))   # Parametry funkce
        ],     
        None # Nepotřebuji definovat body pro tyto funkce, řeším je v interpretu
    ),
    Function(
        'i_to_f',                                           # Název funkce
        Datatype('float'),                                  # Návratový typ
        [
            FunctionParameter('value', Datatype('int'))     # Parametry funkce
        ],     
        None # Nepotřebuji definovat body pro tyto funkce, řeším je v interpretu
    ),
    Function(
        'len',                                              # Název funkce
        Datatype('int'),                                    # Návratový typ
        [
            FunctionParameter('array', ArrayDatatype('any', 1))     # Parametry funkce
        ],     
        None # Nepotřebuji definovat body pro tyto funkce, řeším je v interpretu
    )
]

# str read()
def read() -> str:
    return input()

# void print(str)
def pprint(text: str) -> None:
    print(text)

# int s_to_i(str)
def s_to_i(text: str) -> int:
    try:
        value: int = int(text)
        return value
    except:
        raise Exception(f'Cannot convert str "{text}" to int')

# float s_to_f(str)
def s_to_f(text: str) -> float:
    try:
        value: float = float(text)
        return value
    except:
        raise Exception(f'Cannot convert str "{text}" to float')

# str i_to_s(int)
def i_to_s(value: int) -> str:
    return str(value)

# str f_to_s(int)
def f_to_s(value: float) -> str:
    return str(value)

# int len(array)
def llen(array: list) -> int:
    return len(array)

# float i_to_f(int)
def i_to_f(value: int) -> float:
    return float(value)

# int f_to_i(float)
def f_to_i(value: float) -> int:
    return int(value)

executables: dict[str, callable] = {
    'read': read,
    'print': pprint,
    's_to_i': s_to_i,
    's_to_f': s_to_f,
    'i_to_s': i_to_s,
    'f_to_s': f_to_s,
    'i_to_f': i_to_f,
    'f_to_i': f_to_i,
    'len': llen
}