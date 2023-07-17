from .interpreter import Interpreter
from .context import Context
from .error import is_SLerr
from .vars import Variables
from .lexer import Lexer


def run_file(fp: str, vars_: Variables = None):
    """run shitlang code from file"""
    context = Context(fp)
    code = open(fp, "r").read()

    if vars_ is None:
        vars_ = Variables(context)

    tokens = Lexer(code, context).tokenize()
    if is_SLerr(tokens):
        return tokens

    return Interpreter(tokens, vars_, context).interpret()


def run(code: str, fn: str = "python", vars_: Variables = None):
    """run shitlang code from code (lacks function functionality)"""
    context = Context(fn, is_name=True)

    if vars_ is None:
        vars_ = Variables(context)

    tokens = Lexer(code, context).tokenize()
    if is_SLerr(tokens):
        return tokens

    return Interpreter(tokens, vars_, context).interpret()
