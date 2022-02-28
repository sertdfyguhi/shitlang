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
                    func = token.value[0]

                    if token.value[0] in RESERVED:
                        func = token.value[0] + '_'
                    i = Interpreter(token.value[1], self.vars).interpret(True)
                    if isinstance(i, Error): return i

                    try:
                        r = (f := getattr(self.builtins, func))(*i)
                        if isinstance(r, Error): return r
                    except TypeError as e:
                        print(e)
                        if len(i) > (f.__code__.co_argcount - 1):
                            return Error('TypeError', f'{token.value[0]}() given more arguments than expected')
                        else:
                            return Error('TypeError', f'{token.value[0]}() missing required arguments')

                    res.append(r if token.value[0] != 'return' else [r, 'return'])

                    if type(res[-1]) == list and len(res[-1]) > 1 and res[-1][1] == 'return':
                        if args: res[-1] = res[-1][0]
                        break
                except AttributeError:
                    return Error('BuiltinError', f'no builtin named {token.value[0]}')
                except RecursionError:
                    return Error('RecursionError', 'maximum recursion depth exceeded')
            elif token.type == TT_ARRAY:
                r = Interpreter(token.value, self.vars).interpret()
                if isinstance(r, Error): return r

                res.append(r)
            elif token.type == TT_COMMA:
                continue
            else:
                res.append(token.value)

        return res