TT_FUNC_CALL = 'function call'
TT_STRING = 'string'
TT_NUMBER = 'number'
TT_BOOL = 'boolean'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'{self.type}: {repr(self.value)}'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Token):
            return self.value == o

        return self.type == o.type and self.value == o.value