from .token import TT_NONE, Token
from .vars import Variables
from .error import Error
from .lexer import Lexer

class Function:
    def __init__(self, code, params, vars_=Variables(), allow_use_vars=False) -> None:
        self.code = code
        self.params = params
        self.orig_vars = vars_
        self.allow_use_vars = allow_use_vars

    def run(self, *args):
        self.vars = Variables() if not self.allow_use_vars else self.orig_vars.copy(self.allow_use_vars)

        if len(args) < len(self.params):
            return Error('TypeError', 'function missing arguments')
        elif len(args) > len(self.params):
            return Error('TypeError', 'function given more arguments than expected')

        if not hasattr(self, 'tokens'):
            self.tokens = Lexer(self.code).tokenize()

        if isinstance(self.tokens, Error):
            return self.tokens

        for param, arg in zip(self.params, args):
            self.vars.set(param, arg)

        from .interpreter import Interpreter

        res = Interpreter(self.tokens, self.vars).interpret()
        if isinstance(res, Error): return res

        return Token(TT_NONE) if len(res) == 0 or type(res[-1]) != list else res[-1]

    def __repr__(self) -> str:
        return f'function: <{", ".join(self.params)}>'