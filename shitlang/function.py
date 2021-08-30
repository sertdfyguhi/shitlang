from .vars import Variables
from .error import Error
from .lexer import Lexer

class Function:
    def __init__(self, code, params) -> None:
        self.code = code
        self.params = params

    def run(self, *args):
        if len(args) < len(self.params):
            return Error('TypeError', 'function missing arguments')
        elif len(args) > len(self.params):
            return Error('TypeError', 'function given more arguments than expected')

        if not hasattr(self, 'lexer'):
            self.lexer = Lexer(self.code).tokenize()

        if isinstance(self.lexer, Error):
            return self.lexer

        var = Variables()

        for arg, param in zip(args, self.params):
            var.set(param, arg)

        from .interpreter import Interpreter

        res = Interpreter(self.lexer, var).interpret()

        if isinstance(res, Error):
            return res

        return res[-1][0] if type(res[-1]) == list else None

    def __repr__(self) -> str:
        return f'function: ({", ".join(self.params)})'