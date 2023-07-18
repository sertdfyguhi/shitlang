from .builtins.utils import run_builtin
from .utils import ReturnedValue
from .builtins import Builtins
from .context import Context
from .vars import Variables
from .token import *
from .error import *

RETURN_FUNC_NAMES = ["while", "if"]


class Interpreter:
    def __init__(self, tokens: list[Token], vars_: Variables, context: Context) -> None:
        self.vars = vars_
        self.tokens = tokens
        self.context = context
        self.builtins = Builtins(self.vars, context)

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
                    # fmt: on

                    if is_SLerr(args):
                        return args

                    ret = run_builtin(orig_name, args, self.builtins)
                    if is_SLerr(ret):
                        return ret

                    if orig_name == "return" and not in_args:
                        res.append(ReturnedValue(ret))
                        break
                    else:
                        res.append(ret)
                except RecursionError:
                    return SLRecursionError(
                        self.context, "maximum recursion depth exceeded"
                    )
            elif token.type == TT_ARRAY:
                # fmt: off
                array = Interpreter(
                    token.value,
                    self.vars,
                    self.context
                ).interpret(in_args=True)
                # fmt: on

                if is_SLerr(array):
                    return array

                res.append(array)
            else:
                res.append(token.value)

        # print(f"{self.context}: {res}")

        return res
