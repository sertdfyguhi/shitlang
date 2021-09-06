from .error import Error
from .builtins import Builtins
from .token import *

RESERVED = [
    'not',
    'and',
    'or',
    'return',
    'while'
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
                    func = token.value[0]

                    if token.value[0] in RESERVED:
                        func = token.value[0] + '_'
                    i = Interpreter(token.value[1], self.vars).interpret()
                    if isinstance(i, Error): return i

                    r = getattr(self.builtins, func)(*i)
                    if isinstance(r, Error): return r

                    res.append(r if func != 'return_' else [r, 'return'])

                    if func == 'return_':
                        break

                except TypeError as e:
                    if 'missing' in str(e):
                        return Error('TypeError', f'{token.value[0]}() missing required arguments')
                    else:
                        return Error('TypeError', f'{token.value[0]}() given more arguments than expected')
                except AttributeError:
                    return Error('BuiltinError', f'no builtin named {token.value[0]}')
                except RecursionError:
                    return Error('RecursionError', 'maximum recursion depth exceeded')
            elif token.type == TT_ARRAY:
                r = Interpreter(token.value, self.vars).interpret()
                if isinstance(r, Error): return r

                res.append(r)
            else:
                if token.type == TT_COMMA: continue
                res.append(token.value)

        return res