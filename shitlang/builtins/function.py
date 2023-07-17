from .utils import create_typeerror
from ..function import Function
from ..context import Context
from ..error import *

import os


class FunctionBuiltins:
    def function(self, file, params=[], allow_use_vars=False):
        if self.context.fd is None:
            return SLValueError(
                self.context, "functions are not available in this context"
            )

        file = os.path.join(self.context.fd, file)

        if type(file) != str:
            return create_typeerror(self.context, "file", "string")
        elif type(params) != list or any(type(p) != str for p in params):
            return create_typeerror(self.context, "params", "array of strings")
        elif type(allow_use_vars) != bool:
            return create_typeerror(self.context, "allow_use_vars", "boolean")
        elif not os.path.exists(file):
            return SLFileNotFoundError(self.context, f"file {file!r} not found")

        return Function(
            open(file).read(),
            params,
            Context(file),
            self.vars,
            allow_use_vars,
        )

    def run(self, func, args=[]):
        print(func)
        if not isinstance(func, Function):
            return create_typeerror(self.context, "func", "function")
        elif type(args) != list:
            return create_typeerror(self.context, "args", "array")

        if len(args) < len(func.params):
            return SLValueError(
                self.context, f"function '{func.context.fn}' missing arguments"
            )
        elif len(args) > len(func.params):
            return SLValueError(
                self.context, "function given more arguments than expected"
            )

        ret = func.run(*args)
        if is_SLerr(ret):
            return ret

        return ret[0] if type(ret) == list else None

    def return_(self, value=None):
        return value

    def run_builtin(self, name, args):
        if type(name) != str:
            return create_typeerror(self.context, "name", "string")
        elif type(args) != list:
            return create_typeerror(self.context, "args", "array")

        try:
            func = getattr(self, name, None)
            if func is None:
                return SLBuiltinError(self.context, f"no builtin named {name}")

            return func(*args)
        except TypeError:
            if len(args) > (func.__code__.co_argcount - 1):
                return SLTypeError(
                    self.context, f"{name}() given more arguments than expected"
                )
            else:
                return SLTypeError(self.context, f"{name}() missing required arguments")

    def while_(self, condition, loop):
        if (
            not isinstance(condition, Function)
            or not isinstance(loop, Function)
            or len(condition.params) > 0
            or len(loop.params) > 0
        ):
            return SLTypeError(
                self.context,
                "arguments 'condition' and 'loop' must be a function with no parameters",
            )

        condition.allow_use_vars = True
        loop.allow_use_vars = True

        cond = condition.run()
        if is_SLerr(cond):
            return cond

        print(cond)

        # TODO: refactor
        while cond[0] if type(cond) == list else cond:
            res = loop.run()
            if is_SLerr(res):
                return res

            print(res)

            if res is not None:
                return [res, "return"]

            cond = condition.run()
            if is_SLerr(cond):
                return cond

    def if_(self, condition, func, else_=None):
        if (
            not isinstance(condition, Function)
            or not isinstance(func, Function)
            or len(condition.params) > 0
            or len(func.params) > 0
        ):
            return SLTypeError(
                self.context,
                "arguments 'condition' and 'func' must be a function with no parameters",
            )
        elif else_ and (not isinstance(else_, Function) or len(else_.params) > 0):
            return SLTypeError(
                self.context, "argument 'else' must be a function with no parameters"
            )

        condition.allow_use_vars = True
        func.allow_use_vars = True
        if else_:
            else_.allow_use_vars = True

        cond = condition.run()
        if is_SLerr(cond):
            return cond

        # wtf is this
        # TODO: refactor
        res = func if (None if type(cond) != list else cond[0]) else else_
        if res:
            res = res.run()
            if is_SLerr(res):
                return res

            return [res, "return"]
