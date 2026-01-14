from .builtins.utils import run_builtin
from .environment import Environment
from .utils import ReturnedValue
from .function import Function
from .builtins import Builtins
from .context import Context
from .vars import Variables
from .token import *
from .error import *

RETURN_FUNC_NAMES = ["while", "if"]


class Interpreter:
    def __init__(
        self,
        tokens: list[Token],
        vars_: Variables,
        context: Context,
        environment: Environment,
    ) -> None:
        self.vars = vars_
        self.tokens = tokens
        self.context = context
        self.environment = environment
        self.builtins = Builtins(self.vars, context, environment)

    def interpret(self, in_args: bool = False):
        res = []

        in_function = False
        func_tokens = []
        func_name = ""

        for token in self.tokens:
            if in_function:
                if token.type == TT_FUNC_DEF_END:
                    self.environment.add_func(func_name, func_tokens)

                    in_function = False
                    func_tokens = []
                    func_name = ""
                else:
                    func_tokens.append(token)

                continue

            if token.type == TT_FUNC_CALL:
                try:
                    orig_name = token.value[0]

                    # fmt: off
                    args = Interpreter(
                        token.value[1],
                        self.vars,
                        self.context,
                        self.environment,
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
                    self.context,
                    self.environment,
                ).interpret(in_args=True)
                # fmt: on

                if is_SLerr(array):
                    return array

                res.append(array)
            elif token.type == TT_FUNC_DEF:
                in_function = True
                func_name = token.value
            else:
                res.append(token.value)

        # print(f"{self.context}: {res}")
        # print(self.environment.functions)

        return res
