from .builtins import Builtins
from .context import Context
from .vars import Variables
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
    def __init__(self, tokens: list[Token], vars_: Variables, context: Context) -> None:
        self.context = context
        self.tokens = tokens
        self.vars = vars_
        self.builtins = Builtins(self.vars, self.context)

    def interpret(self, in_args: bool = False):
        res = []

        for token in self.tokens:
            if token.type == TT_FUNC_CALL:
                try:
                    orig_name = token.value[0]

                    # fmt: off
                    args = Interpreter(
                        token.value[1],
                        self.vars,
                        self.context
                    ).interpret(in_args=True)
                    # print(token.value[1])
                    print(args)

                    if is_SLerr(args):
                        return args
                    # fmt: on

                    try:
                        builtin = getattr(
                            self.builtins,
                            orig_name + "_" if orig_name in RESERVED else orig_name,
                        )
                    except AttributeError:
                        return SLBuiltinError(
                            self.context, f"no builtin named {orig_name}"
                        )

                    try:
                        ret = builtin(*args)
                        if is_SLerr(ret):
                            return ret
                    except TypeError as e:
                        # TODO: refactor
                        # .__code__.co_argcount is how many parameters the function has
                        # len(.__defaults__) is the amount of optional parameters
                        if len(args) > (builtin.__code__.co_argcount - 1):
                            return SLTypeError(
                                self.context,
                                f"{orig_name}() given more args than expected",
                            )
                        elif len(args) < (
                            builtin.__code__.co_argcount
                            - len(builtin.__defaults__ or [0])
                        ):
                            return SLTypeError(
                                self.context,
                                f"{orig_name}() missing required args",
                            )
                        else:
                            raise e

                    res.append(
                        ret
                        if orig_name != "return" and not in_args
                        else [ret, "return"]
                    )

                    if orig_name == "return":
                        break
                except RecursionError:
                    return SLRecursionError(
                        self.context, "maximum recursion depth exceeded"
                    )
            elif token.type == TT_ARRAY:
                # do the parsing in lexer
                array = Interpreter(token.value, self.vars, self.context).interpret()
                if is_SLerr(array):
                    return array

                res.append(array)
            else:
                res.append(token.value)

        return res
