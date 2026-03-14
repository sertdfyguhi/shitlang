from ..function import Function
from .utils import run_builtin
from ..context import Context
from ..error import *

import os


def get_shit_file(file: str, context: Context):
    if context.fd is None:
        raise SLFileNotFoundError(
            context,
            f"function {file!r} not found, cannot use files for functions in this context",
        )

    file_path = os.path.join(context.fd, file)

    if not os.path.isfile(file_path):
        raise SLFileNotFoundError(
            context, f"function {file!r} not found or is not a file"
        )

    with open(file_path, "r") as f:
        return f.read(), Context(file_path)


class FunctionBuiltins:
    def function(self, file: str, params: list[str] = [], allow_use_vars: bool = False):
        if self.environment.has_func(file):
            code = self.environment.get_func(file)
            context = self.context
        else:
            code, context = get_shit_file(file, self.context)

        return Function(
            code,
            params,
            context,
            self.environment,
            self,
            self.vars,
            allow_use_vars,
        )

    def run(self, func: Function, args: list = []):
        if len(args) < len(func.params):
            raise SLValueError(
                self.context, f"function {func.context.fn!r} missing arguments"
            )
        elif len(args) > len(func.params):
            raise SLValueError(
                self.context,
                f"function {func.context.fn!r} given more arguments than expected",
            )

        return func.run(*args)

    # def import_(self, file: str, namespace: str):
    #     code, context = get_shit_file(file, self.context)

    def run_builtin(self, name: str, args: list):
        return run_builtin(name, args, self)

    def while_(self, condition: Function, loop: Function):
        if len(condition.params) > 0 or len(loop.params) > 0:
            raise SLTypeError(
                self.context,
                "arguments 'condition' and 'loop' must have no parameters",
            )

        condition.allow_use_vars = True
        loop.allow_use_vars = True

        cond = condition.run()
        while cond:
            ret = loop.run()

            # return error / result if loop returns
            if ret is not None:
                return ret

            cond = condition.run()

    def if_(self, condition: Function, func: Function, else_: Function | None = None):
        if len(condition.params) > 0 or len(func.params) > 0:
            raise SLTypeError(
                self.context,
                "arguments 'condition' and 'func' must have no parameters",
            )

        if else_ and len(else_.params) > 0:
            raise SLTypeError(self.context, "argument 'else' must have no parameters")

        condition.allow_use_vars = True
        func.allow_use_vars = True
        if else_:
            else_.allow_use_vars = True

        if condition.run():
            func.run()
        elif else_:
            else_.run()

    def try_(self, func: Function, catch_func: Function):
        if len(func.params) > 0:
            raise SLTypeError(self.context, "argument 'func' must have no parameters")
        elif len(catch_func.params) != 1:
            raise SLTypeError(
                self.context, "argument 'catch_func' must have 1 parameter"
            )

        try:
            func.run()
        except SLError as err:
            catch_func.run(err.details)
