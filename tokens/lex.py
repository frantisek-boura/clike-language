PATTERNS = [
    (r'\s+', None),             # Bílé znaky (mezery, tabulátory, nové řádky)
    (r'//.*', None),            # Jednořádkové komentáře
    (r'/\*.*?\*/', None),       # Víceřádkové komentáře
    (r'\bconst\b', 'const'),
    (r'\{', '{'),
    (r'\}', '}'),
    (r'\(', '('),
    (r'\)', ')'),
    (r'\[', '['),
    (r'\]', ']'),
    (r'\bif\b', 'if'),
    (r'\belse\b', 'else'),
    (r'\bbreak\b', 'break'),
    (r'\breturn\b', 'return'),
    (r'\bfor\b', 'for'),
    (r'\bint\b', 'int'),
    (r'\bstr\b', 'str'),
    (r'\bfloat\b', 'float'),
    (r'\bvoid\b', 'void'),
    (r'\d+\.\d*', 'lit_float'), # Desetinná čísla
    (r'\d+', 'lit_int'),        # Celá čísla
    (r'"[^"]*"', 'lit_str'),    # Řetězce v uvozovkách 
    (r'\w[\w\d]*', 'name'),     # Identifikátory
    (r'!=', '!='),
    (r'==', '=='),
    (r'<=', '<='),
    (r'>=', '>='),
    (r'<', '<'),
    (r'>', '>'),
    (r'\+', '+'),
    (r'-', '-'),
    (r'\*', '*'),
    (r'/', '/'),
    (r'=', '='),
    (r',', ','),
    (r';', ';'),
    (r'@', '@')
]