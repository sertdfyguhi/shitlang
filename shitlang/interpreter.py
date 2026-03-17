from .builtins.utils import run_builtin
from .environment import Environment
from .utils import ReturnedValue
from .builtins import Builtins
from .function import Function
from .context import Context
from .vars import Variables
from .token import *
from .error import *

RETURN_FUNC_NAMES = ["while", "if"]


class Interpreter:
    def __init__(
        self,
        context: Context,
        vars_: Variables = None,
        environment: Environment = None,
        builtins: Builtins = None,
    ) -> None:
        self.context = context

        self.vars = Variables(context) if vars_ is None else vars_
        self.environment = Environment(context) if environment is None else environment
        self.builtins = (
            Builtins(self.vars, context, self.environment)
            if builtins is None
            else builtins
        )

    def interpret(self, tokens: list[Token]):
        res = []

        for token in tokens:
            self.context.pos = token.start_pos
            self.context.end_pos = token.end_pos

            if token.type == TT_FUNC_CALL:
                args = self.interpret(token.value[1])

                if token.value[0] == "return":
                    res.append(ReturnedValue(None if len(args) == 0 else args[0]))
                    break

                # reset to the start of function call after interpreting args
                self.context.pos = token.start_pos
                self.context.end_pos = token.end_pos

                try:
                    ret = run_builtin(token.value[0], args, self.builtins)
                except SLError as err:
                    err.details = f"{token.value[0]}() {err.details}"
                    raise err

                res.append(ret)
            elif token.type == TT_LAMBDA_DEF:
                params = ["_" * (n + 1) for n in range(token.value[1])]
                lambda_func = Function(
                    token.value[0],
                    params,
                    self.context,
                    self.environment,
                    self.builtins,
                    self.vars,
                )
                res.append(lambda_func)
            elif token.type == TT_ARRAY:
                res.append(self.interpret(token.value))
            elif token.type == TT_FUNC_DEF:
                self.environment.add_func(token.value[0], token.value[1])
            elif token.type == TT_UNDERSCORE:
                raise SLSyntaxError(self.context, "unexpected underscore")
            else:
                res.append(token.value)

        return res
