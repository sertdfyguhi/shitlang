from .interpreter import Interpreter
from .error import Error
from .vars import Variables
from .lexer import Lexer

def run(code, fn, vars=None):
    if not vars: vars = Variables(fn)
    lexer = Lexer(code, fn)
    tokens = lexer.tokenize()
    # return tokens

    if isinstance(tokens, Error): return tokens

    interpreter = Interpreter(tokens, vars, fn)
    return interpreter.interpret()