from .error import *

class Variables:
    def __init__(self, fn, d={}) -> None:
        self.fn = fn
        self.vars = d

    def set(self, name, value):
        self.vars[name] = value

    def get(self, name):
        if name not in self.vars:
            return VarNotDefinedError_(self.fn, f'variable "{name}" not defined')
        return self.vars[name]

    def delete(self, name):
        if name not in self.vars:
            return VarNotDefinedError_(self.fn, f'variable "{name}" not defined')
        del self.vars[name]

    def copy(self, allow_use_vars=False):
        return Variables(self.fn, self.vars.copy() if not allow_use_vars else self.vars)