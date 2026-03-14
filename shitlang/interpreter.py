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

        func_tokens = []
        func_name = ""

        for token in tokens:
            if func_name:
                if token.type == TT_FUNC_DEF_END:
                    self.environment.add_func(func_name, func_tokens)

                    func_tokens = []
                    func_name = ""
                else:
                    func_tokens.append(token)

                continue

            if token.type == TT_FUNC_CALL:
                orig_name = token.value[0]

                args = self.interpret(token.value[1])

                if orig_name == "return":
                    res.append(ReturnedValue(None if len(args) == 0 else args[0]))
                    break

                ret = run_builtin(orig_name, args, self.builtins)
                res.append(ret)
            elif token.type == TT_ARRAY:
                array = self.interpret(token.value)
                res.append(array)
            elif token.type == TT_FUNC_DEF:
                func_name = token.value
            elif token.type == TT_UNDERSCORE:
                raise SLSyntaxError(self.context, "unexpected underscore")
            else:
                res.append(token.value)

        return res
