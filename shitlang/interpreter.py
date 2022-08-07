from .builtins import Builtins
from .error import *
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
    def __init__(self, tokens, vars, fn) -> None:
        self.tokens = tokens
        self.vars = vars
        self.fn = fn
        self.builtins = Builtins(self.vars, self.fn)

    def interpret(self, args=False):
        res = []

        for token in self.tokens:
            if token.type == TT_FUNC_CALL:
                try:
                    name = token.value[0] + '_' if token.value[0] in RESERVED else token.value[0]

                    arguments = Interpreter(token.value[1], self.vars, self.fn).interpret(True)
                    if isinstance(arguments, Error): return arguments

                    try:
                        returned = (builtin := getattr(self.builtins, name))(*arguments)
                        if isinstance(returned, Error): return returned
                    except TypeError as e:
                        # .__code__.co_argcount is how many parameters the function has
                        # len(.__defaults__) is the amount of optional parameters
                        if len(arguments) > (builtin.__code__.co_argcount - 1):
                            return TypeError_(self.fn, f'{token.value[0]}() given more arguments than expected')
                        elif len(arguments) < (builtin.__code__.co_argcount - len(builtin.__defaults__ or [0])):
                            return TypeError_(self.fn, f'{token.value[0]}() missing required arguments')
                        else: raise e

                    res.append(returned if token.value[0] != 'return' else [returned, 'return'])

                    if type(res[-1]) == list and len(res[-1]) > 1 and res[-1][1] == 'return':
                        if args: res[-1] = res[-1][0]
                        break
                except AttributeError:
                    return BuiltinError_(self.fn, f'no builtin named {token.value[0]}')
                except RecursionError:
                    return RecursionError_(self.fn, 'maximum recursion depth exceeded')
            elif token.type == TT_ARRAY:
                array = Interpreter(token.value, self.vars, self.fn).interpret()
                if isinstance(array, Error): return array

                res.append(array)
            elif token.type == TT_COMMA:
                continue
            else:
                res.append(token.value)

        return res