class Token:
    def __init__(self, type: str, value: str):
        self.type: str = type
        self.value: str = value

    def __str__(self):
        return f'type: {self.type}, value: {self.value}'