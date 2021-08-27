from shitlang.error import Error

class Variables:
    def __init__(self) -> None:
        self.vars = {}

    def set(self, key, value):
        self.vars[key] = value

    def get(self, key):
        if key not in self.vars:
            return Error('VarNotDefinedError', f'variable "{key}" not defined')
        return self.vars[key]

    def delete(self, key):
        if key not in self.vars:
            return Error('VarNotDefinedError', f'variable "{key}" not defined')
        del self.vars[key]