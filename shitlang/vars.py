from .error import Error

class Variables:
    def __init__(self, d={}) -> None:
        self.vars = d

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

    def copy(self, allow_use_vars=False):
        return Variables(self.vars.copy() if not allow_use_vars else self.vars)