from .environment import Environment
from .interpreter import Interpreter
from .context import Context
from .error import is_SLerr
from .vars import Variables
from .lexer import Lexer


def _run(code: str, context: Context, vars_: Variables = None):
    if vars_ is None:
        vars_ = Variables(context)

    tokens = Lexer(code, context).tokenize()
    if is_SLerr(tokens):
        return tokens

    # print(tokens)

    environment = Environment(context)
    return Interpreter(tokens, vars_, context, environment).interpret()


def run_file(fp: str, vars_: Variables = None):
    """run shitlang code from file"""
    code = open(fp, "r").read()
    context = Context(fp)

    return _run(code, context, vars_)


def run(code: str, fn: str = "python", vars_: Variables = None):
    """run shitlang code from code (lacks function functionality)"""
    context = Context(fn, is_name=True)
    return _run(code, context, vars_)
