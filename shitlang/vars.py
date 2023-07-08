from .error import *


class Variables:
    def __init__(self, fn, vardict={}) -> None:
        self.fn = fn
        self.vars = vardict

    def set(self, name, value):
        self.vars[name] = value

    def get(self, name):
        if name not in self.vars:
            return SLVarNotDefinedError(self.fn, f'variable "{name}" not defined')

        return self.vars[name]

    def delete(self, name):
        if name not in self.vars:
            return SLVarNotDefinedError(self.fn, f'variable "{name}" not defined')

        del self.vars[name]

    def copy(self, allow_use_vars=False):
        return Variables(self.fn, self.vars if allow_use_vars else self.vars.copy())
