from tokens.toktype import Token

class PeekableIter:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.index: int = 0

    def peek(self) -> Token | None:
        if self.index >= len(self.tokens):
            return None
        return self.tokens[self.index]

    def next(self) -> Token:
        if self.index >= len(self.tokens):
            return None
        current: Token = self.tokens[self.index]
        self.index += 1
        return current
