from .builtins import Builtins
from .token import *
from .error import *

RETURN_FUNC_NAMES = ["while", "if"]

RESERVED = [
    "not",
    "and",
    "or",
    "return",
    "while",
    "if",
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
                    orig_name = token.value[0]

                    args = Interpreter(token.value[1], self.vars, self.fn).interpret(
                        True
                    )
                    if is_SLerr(args):
                        return args

                    try:
                        builtin = getattr(
                            self.builtins,
                            orig_name + "_" if orig_name in RESERVED else orig_name,
                        )
                    except AttributeError:
                        return SLBuiltinError(self.fn, f"no builtin named {orig_name}")

                    try:
                        ret = builtin(*args)
                        if is_SLerr(ret):
                            return ret
                    # TODO: hwo does thi work
                    except TypeError as e:
                        # .__code__.co_argcount is how many parameters the function has
                        # len(.__defaults__) is the amount of optional parameters
                        if len(args) > (builtin.__code__.co_argcount - 1):
                            return SLTypeError(
                                self.fn,
                                f"{orig_name}() given more args than expected",
                            )
                        elif len(args) < (
                            builtin.__code__.co_argcount
                            - len(builtin.__defaults__ or [0])
                        ):
                            return SLTypeError(
                                self.fn,
                                f"{orig_name}() missing required args",
                            )
                        else:
                            raise e

                    res.append(ret if orig_name != "return" else [ret, "return"])

                    if (
                        type(res[-1]) == list
                        and len(res[-1]) > 1
                        and res[-1][1] == "return"
                    ):
                        if args:
                            res[-1] = res[-1][0]
                        break
                except RecursionError:
                    return SLRecursionError(self.fn, "maximum recursion depth exceeded")
            elif token.type == TT_ARRAY:
                array = Interpreter(token.value, self.vars, self.fn).interpret()
                if is_SLerr(array):
                    return array

                res.append(array)
            elif token.type == TT_COMMA:
                continue
            else:
                res.append(token.value)

        return res
