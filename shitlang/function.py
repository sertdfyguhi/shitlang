from .environment import Environment
from .utils import ReturnedValue
from .context import Context
from .vars import Variables
from .lexer import Lexer
from .error import *


class Function:
    def __init__(
        self,
        code: str | list,
        params,
        context: Context,
        environment: Environment,
        builtins,
        vars_: Variables = None,
        allow_use_vars: bool = False,
    ) -> None:
        # TODO: wtf
        self.code = code
        if type(self.code) == list:
            self.tokens = code

        self.params = params
        self.context = context
        self.environment = environment
        self.builtins = builtins
        self.orig_vars = vars_.copy() if vars_ else Variables(context)
        self.orig_vars.context = context
        self.allow_use_vars = allow_use_vars

    def run(self, *args):
        self.vars = (
            Variables(self.context)
            if not self.allow_use_vars
            else self.orig_vars.copy(self.allow_use_vars)
        )

        if not hasattr(self, "tokens"):
            self.tokens = Lexer(self.code, self.context).tokenize()

        for param, arg in zip(self.params, args):
            self.vars.set(param, arg)

        # to avoid circular import
        from .interpreter import Interpreter

        res = Interpreter(
            self.context, self.vars, self.environment, self.builtins
        ).interpret(self.tokens)
        if len(res) > 0 and isinstance(res[-1], ReturnedValue):
            return res[-1].value

    def __repr__(self) -> str:
        return f'function: <{", ".join(self.params)}>'
