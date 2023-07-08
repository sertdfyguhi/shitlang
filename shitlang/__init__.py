from .interpreter import Interpreter
from .error import is_SLerr
from .vars import Variables
from .lexer import Lexer


def run(code, fn, vars=None):
    if vars is None:
        vars = Variables(fn)

    tokens = Lexer(code, fn).tokenize()
    return tokens

    # if is_SLerr(tokens):
    #     return tokens

    # return Interpreter(tokens, vars, fn).interpret()
