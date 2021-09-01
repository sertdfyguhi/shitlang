from .error import Error
from .builtins import Builtins
from .token import *

RESERVED = [
    'not',
    'and',
    'or',
    'return'
]

class Interpreter:
    def __init__(self, tokens, vars) -> None:
        self.tokens = tokens
        self.vars = vars
        self.builtins = Builtins(self.vars)

    def interpret(self):
        res = []

        for token in self.tokens:
            if token.type == TT_FUNC_CALL:
                try:
                    if token.value[0] in RESERVED:
                        token.value[0] = token.value[0] + '_'
                    i = Interpreter(token.value[1], self.vars).interpret()
                    if isinstance(i, Error): return i

                    r = getattr(self.builtins, token.value[0])(*i)
                    if isinstance(r, Error): return r

                    res.append(r if token.value[0] != 'return_' else [r, 'return'])

                    if token.value[0] == 'return_':
                        break

                except TypeError as e:
                    if 'missing' in str(e):
                        return Error('TypeError', f'{token.value[0]}() missing required arguments')
                    else:
                        return Error('TypeError', f'{token.value[0]}() given more arguments than expected')
                except AttributeError:
                    return Error('BuiltinError', f'no builtin named {token.value[0]}')
            elif token.type == TT_ARRAY:
                r = Interpreter(token.value, self.vars).interpret()
                if isinstance(r, Error): return r

                res.append(r)
            else:
                res.append(token.value)

        return res