from .error import Error

class Variables:
    def __init__(self, d={}) -> None:
        self.vars = d

    def set(self, name, value):
        self.vars[name] = value

    def get(self, name):
        if name not in self.vars:
            return Error('VarNotDefinedError', f'variable "{name}" not defined')
        return self.vars[name]

    def delete(self, name):
        if name not in self.vars:
            return Error('VarNotDefinedError', f'variable "{name}" not defined')
        del self.vars[name]

    def copy(self, allow_use_vars=False):
        return Variables(self.vars.copy() if not allow_use_vars else self.vars)