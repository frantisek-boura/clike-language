from tokens.lex import PATTERNS
from tokens.toktype import Token
import re

def get_tokens(code: str) -> list[Token]:
    tokens = []
    while code:
        for pattern, token_type in PATTERNS:
            match: re.Match | None = re.match(pattern, code)
            if match:
                value: str = match.group(0)
                if token_type is not None:
                    tokens.append(Token(token_type, value))
                code = code[len(value):]
                break
        else:
            raise SyntaxError(f"Unexpected token") 
    return tokens