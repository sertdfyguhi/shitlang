from ..function import Function
from .utils import run_builtin
from ..context import Context
from ..error import *

import os


class FunctionBuiltins:
    def function(self, file: str, params: list[str] = [], allow_use_vars: bool = False):
        code = None
        context = self.context

        if self.environment.has_func(file):
            code = self.environment.get_func(file)
        else:
            if self.context.fd is None:
                return SLFileNotFoundError(
                    self.context,
                    f"function {file!r} not found, cannot use files for functions in this context",
                )

            file_path = os.path.join(self.context.fd, file)

            if os.path.exists(file_path):
                with open(file_path) as f:
                    code = f.read()

                context = Context(file_path)
            else:
                return SLFileNotFoundError(self.context, f"function {file!r} not found")

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
            return SLValueError(
                self.context, f"function '{func.context.fn}' missing arguments"
            )
        elif len(args) > len(func.params):
            return SLValueError(
                self.context,
                f"function '{func.context.fn}' given more arguments than expected",
            )

        ret = func.run(*args)
        if is_SLerr(ret):
            return ret

        return ret

    def return_(self, value=None):
        return value

    def run_builtin(self, name: str, args: list):
        return run_builtin(name, args, self)

    def while_(self, condition: Function, loop: Function):
        if len(condition.params) > 0 or len(loop.params) > 0:
            return SLTypeError(
                self.context,
                "arguments 'condition' and 'loop' must have no parameters",
            )

        condition.allow_use_vars = True
        loop.allow_use_vars = True

        cond = condition.run()
        if is_SLerr(cond):
            return cond

        while cond:
            ret = loop.run()

            # return error / result if loop returns
            if ret is not None:
                return ret

            cond = condition.run()
            if is_SLerr(cond):
                return cond

    def if_(self, condition: Function, func: Function, else_: Function | None = None):
        if len(condition.params) > 0 or len(func.params) > 0:
            return SLTypeError(
                self.context,
                "arguments 'condition' and 'func' must have no parameters",
            )

        if else_ and len(else_.params) > 0:
            return SLTypeError(self.context, "argument 'else' must have no parameters")

        condition.allow_use_vars = True
        func.allow_use_vars = True
        if else_:
            else_.allow_use_vars = True

        cond = condition.run()
        if is_SLerr(cond):
            return cond

        ret = None

        # check if returned result of condition is truthy
        if cond:
            ret = func.run()
        elif else_ is not None:
            ret = else_.run()

        if is_SLerr(ret):
            return ret

    def try_(self, func: Function, catch_func: Function):
        if len(func.params) > 0:
            return SLTypeError(self.context, "argument 'func' must have no parameters")
        elif len(catch_func.params) != 1:
            return SLTypeError(
                self.context, "argument 'catch_func' must have 1 parameter"
            )

        ret = func.run()
        if is_SLerr(ret):
            catch_func.run(ret.details)
