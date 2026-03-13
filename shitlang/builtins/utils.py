from ..context import Context
from ..error import *

from beartype.roar import BeartypeCallHintParamViolation
import re


RESERVED_BUILTINS = [
    "not",
    "and",
    "or",
    "return",
    "while",
    "if",
    "try",
]


def run_builtin(name: str, args: list, builtins):
    try:
        builtin = getattr(
            builtins, name + "_" if name in RESERVED_BUILTINS else name, None
        )
        if builtin is None:
            return SLBuiltinError(builtins.context, f"no builtin named '{name}'")

        return builtin(*args)
    except TypeError as err:
        # TODO: refactor to use inspect.signature or smth
        # .__code__.co_argcount is how many parameters the function has
        # len(.__defaults__) is the amount of optional parameters
        argcount = builtin.__code__.co_argcount - 1  # remove self

        if len(args) > argcount:
            return SLTypeError(
                builtins.context,
                f"{name}() given {len(args) - argcount} more args than expected",
            )
        elif len(args) < (argcount - len(builtin.__defaults__ or [])):
            return SLTypeError(
                builtins.context,
                f"{name}() missing required args",
            )
        else:
            return SLTypeError(builtins.context, str(err))
    except BeartypeCallHintParamViolation as err:
        message = str(err)
        message = message.replace("type hint", "type")
        message = message.replace("Method", "Builtin")
        message = message.replace("shitlang.builtins.", "")
        message = message.replace("list", "array")

        return SLTypeError(builtins.context, message)
    except RecursionError:
        return SLRecursionError(builtins.context, "maximum recursion depth exceeded")
    except Exception as err:
        return SLError(type(err).__name__, builtins.context, str(err))


def create_typeerror(context: Context, name: str | list[str], type_: str | list[str]):
    is_list = isinstance(name, list)
    if is_list:
        name = "' and '".join(name)

    if type(type_) == list:
        type_ = " or ".join(type_)

    return SLTypeError(
        context,
        f"argument{'s' if is_list else ''} '{name}' must be of type {type_}",
    )
