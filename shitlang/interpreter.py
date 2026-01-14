from .builtins.utils import run_builtin
from .environment import Environment
from .utils import ReturnedValue
from .builtins import Builtins
from .context import Context
from .vars import Variables
from .token import *
from .error import *

RETURN_FUNC_NAMES = ["while", "if"]


class Interpreter:
    def __init__(
        self,
        vars_: Variables,
        context: Context,
        environment: Environment,
        builtins: Builtins = None,
    ) -> None:
        self.vars = vars_
        self.context = context
        self.environment = environment

        if builtins is None:
            builtins = Builtins(vars_, context, environment)

        self.builtins = builtins

    def interpret(self, tokens: list[Token], in_args: bool = False):
        res = []

        in_function = False
        func_tokens = []
        func_name = ""

        for token in tokens:
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

                    args = self.interpret(token.value[1], in_args=True)
                    if is_SLerr(args):
                        return args

                    # print(orig_name, token, args)

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
                array = self.interpret(token.value, in_args=True)
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
