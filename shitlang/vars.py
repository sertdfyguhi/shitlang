from .context import Context
from .error import *


class Variables:
    def __init__(self, context: Context, vardict: dict = {}) -> None:
        self.context = context
        self.vars = vardict

    def set(self, name, value):
        self.vars[name] = value

    def get(self, name):
        if name not in self.vars:
            return SLVarNotDefinedError(
                self.context.filename, f'variable "{name}" not defined'
            )

        return self.vars[name]

    def delete(self, name):
        if name not in self.vars:
            return SLVarNotDefinedError(self.context, f'variable "{name}" not defined')

        del self.vars[name]

    def copy(self, allow_use_vars=False):
        return self if allow_use_vars else Variables(self.context, self.vars)
