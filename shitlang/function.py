from .token import TT_NONE, Token
from .vars import Variables
from .lexer import Lexer
from .error import *


class Function:
    def __init__(self, code, params, fn, vars_=None, allow_use_vars=False) -> None:
        # TODO: wtf
        self.code = code
        self.params = params
        self.fn = fn
        self.orig_vars = vars_.copy() if vars_ else Variables(fn)
        self.orig_vars.fn = fn
        self.allow_use_vars = allow_use_vars

    def run(self, *args):
        self.vars = (
            Variables(self.fn)
            if not self.allow_use_vars
            else self.orig_vars.copy(self.allow_use_vars)
        )

        if not hasattr(self, "tokens"):
            self.tokens = Lexer(self.code, self.fn).tokenize()

            if is_SLerr(self.tokens):
                return self.tokens

        for param, arg in zip(self.params, args):
            self.vars.set(param, arg)

        from .interpreter import Interpreter

        res = Interpreter(self.tokens, self.vars, self.fn).interpret()
        if is_SLerr(res):
            return res

        return Token(TT_NONE) if len(res) == 0 or type(res[-1]) != list else res[-1]

    def __repr__(self) -> str:
        return f'function: <{", ".join(self.params)}>'
