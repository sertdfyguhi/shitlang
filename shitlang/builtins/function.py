from .utils import create_typeerror
from ..function import Function
from ..error import *

import os


class FunctionBuiltins:
    def function(self, file, params=[], allow_use_vars=False):
        if type(file) != str:
            return create_typeerror(self.fn, "file", "string")
        elif type(params) != list or any(type(p) != str for p in params):
            return create_typeerror(self.fn, "params", "array of strings")
        elif type(allow_use_vars) != bool:
            return create_typeerror(self.fn, "allow_use_vars", "boolean")
        elif not os.path.exists(file):
            return SLFileNotFoundError(self.fn, f"file {file!r} not found")

        return Function(open(file).read(), params, file, self.vars, allow_use_vars)

    def run(self, func, args=[]):
        if not isinstance(func, Function):
            return create_typeerror(self.fn, "func", "function")
        elif type(args) != list:
            return create_typeerror(self.fn, "args", "array")

        if len(args) < len(func.params):
            return SLValueError(self.fn, "function missing arguments")
        elif len(args) > len(func.params):
            return SLValueError(self.fn, "function given more arguments than expected")

        ret = func.run(*args)
        if is_SLerr(ret):
            return ret

        return ret[0] if type(ret) == list else None

    def return_(self, value=None):
        return value

    def run_builtin(self, name, args):
        if type(name) != str:
            return create_typeerror(self.fn, "name", "string")
        elif type(args) != list:
            return create_typeerror(self.fn, "args", "array")

        try:
            func = getattr(self, name, None)
            if func is None:
                return SLBuiltinError(self.fn, f"no builtin named {name}")

            return func(*args)
        except TypeError:
            if len(args) > (func.__code__.co_argcount - 1):
                return SLTypeError(
                    self.fn, f"{name}() given more arguments than expected"
                )
            else:
                return SLTypeError(self.fn, f"{name}() missing required arguments")

    def while_(self, condition, loop):
        if (
            not isinstance(condition, Function)
            or not isinstance(loop, Function)
            or len(condition.params) > 0
            or len(loop.params) > 0
        ):
            return SLTypeError(
                self.fn,
                "arguments 'condition' and 'loop' must be a function with no parameters",
            )

        condition.allow_use_vars = True
        loop.allow_use_vars = True

        cond = condition.run()
        if is_SLerr(cond):
            return cond

        while cond[0] if type(cond) == list else cond:
            res = loop.run()
            if is_SLerr(res):
                return res

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
                self.fn,
                "arguments 'condition' and 'func' must be a function with no parameters",
            )
        elif else_ and (not isinstance(else_, Function) or len(else_.params) > 0):
            return SLTypeError(
                self.fn, "argument 'else' must be a function with no parameters"
            )

        condition.allow_use_vars = True
        func.allow_use_vars = True
        if else_:
            else_.allow_use_vars = True

        cond = condition.run()
        if is_SLerr(cond):
            return cond

        # wtf is this
        res = func if (None if type(cond) != list else cond[0]) else else_
        if res:
            res = res.run()
            if is_SLerr(res):
                return res

            return [res, "return"]
