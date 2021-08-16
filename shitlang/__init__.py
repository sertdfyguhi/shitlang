from .interpreter import Interpreter
from .error import Error
from .vars import Variables
from .lexer import Lexer

def run(code, vars=Variables()):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    # return tokens

    if isinstance(tokens, Error):
        return tokens

    interpreter = Interpreter(tokens, vars)
    res = interpreter.interpret()
    return res