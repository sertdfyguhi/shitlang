from .environment import Environment
from .interpreter import Interpreter
from .context import Context
from .error import SLError
from .vars import Variables
from .lexer import Lexer


def _run(
    code: str,
    context: Context,
    vars_: Variables = None,
    environment: Environment = None,
):
    tokens = Lexer(code, context).tokenize()
    return Interpreter(context, vars_, environment).interpret(tokens)


def run_file(fp: str, vars_: Variables = None, environment: Environment = None):
    """run shitlang code from file"""
    code = open(fp, "r").read()
    context = Context(fp)

    return _run(code, context, vars_, environment)


def run(
    code: str,
    fn: str = "python",
    vars_: Variables = None,
    environment: Environment = None,
):
    """run shitlang code from code"""
    context = Context(fn, is_name=True)

    if environment is None:
        environment = Environment(context)

    return _run(code, context, vars_)
