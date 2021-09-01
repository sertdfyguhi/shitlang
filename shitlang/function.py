from .vars import Variables
from .error import Error
from .lexer import Lexer

class Function:
    def __init__(self, code, params, vars_=Variables(), allow_use_vars=False) -> None:
        self.code = code
        self.params = params
        self.vars_original = vars_
        self.allow_use_vars = allow_use_vars

    def run(self, *args):
        self.vars = self.vars_original.copy(self.allow_use_vars)

        if len(args) < len(self.params):
            return Error('TypeError', 'function missing arguments')
        elif len(args) > len(self.params):
            return Error('TypeError', 'function given more arguments than expected')

        if not hasattr(self, 'lexer'):
            self.lexer = Lexer(self.code).tokenize()

        if isinstance(self.lexer, Error):
            return self.lexer

        for arg, param in zip(args, self.params):
            self.vars.set(param, arg)

        from .interpreter import Interpreter

        res = Interpreter(self.lexer, self.vars).interpret()

        if isinstance(res, Error):
            return res

        return res[-1][0] if type(res[-1]) == list else None

    def __repr__(self) -> str:
        return f'function: ({", ".join(self.params)})'