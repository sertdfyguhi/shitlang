from .error import Error
from .builtins import Builtins
from .token import *

RETURN_FUNC_NAMES = [
    'while',
    'if'
]

RESERVED = [
    'not',
    'and',
    'or',
    'return',
    'while',
    'if',
]

class Interpreter:
    def __init__(self, tokens, vars) -> None:
        self.tokens = tokens
        self.vars = vars
        self.builtins = Builtins(self.vars)

    def interpret(self, args=False):
        res = []

        for token in self.tokens:
            if token.type == TT_FUNC_CALL:
                try:
                    name = token.value[0]

                    if token.value[0] in RESERVED:
                        name = token.value[0] + '_'

                    arguments = Interpreter(token.value[1], self.vars).interpret(True)
                    if isinstance(arguments, Error): return arguments

                    try:
                        r = (builtin := getattr(self.builtins, name))(*arguments)
                        if isinstance(r, Error): return r
                    except TypeError as e:
                        # .__code__.co_argcount is how many parameters the function has
                        # len(.__defaults__) gets the amount of optional parameters
                        if len(arguments) > (builtin.__code__.co_argcount - 1):
                            return Error('TypeError', f'{token.value[0]}() given more arguments than expected')
                        elif len(arguments) < (builtin.__code__.co_argcount - len(builtin.__defaults__ or [0])):
                            return Error('TypeError', f'{token.value[0]}() missing required arguments')
                        else: raise e

                    res.append(r if token.value[0] != 'return' else [r, 'return'])

                    if type(res[-1]) == list and len(res[-1]) > 1 and res[-1][1] == 'return':
                        if args: res[-1] = res[-1][0]
                        break
                except AttributeError:
                    return Error('BuiltinError', f'no builtin named {token.value[0]}')
                except RecursionError:
                    return Error('RecursionError', 'maximum recursion depth exceeded')
            elif token.type == TT_ARRAY:
                array = Interpreter(token.value, self.vars).interpret()
                if isinstance(array, Error): return r

                res.append(array)
            elif token.type == TT_COMMA:
                continue
            else:
                res.append(token.value)

        return res