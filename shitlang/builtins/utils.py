from ..context import Context
from ..error import *


RESERVED_BUILTINS = [
    "not",
    "and",
    "or",
    "return",
    "while",
    "if",
]


def run_builtin(name: str, args: list, builtins):
    context = builtins.context

    if name in RESERVED_BUILTINS:
        name += "_"

    try:
        builtin = getattr(builtins, name, None)
        if builtin is None:
            return SLBuiltinError(context, f"no builtin named '{name}'")

        return builtin(*args)
    except TypeError as e:
        # TODO: refactor to use inspect.signature or smth
        # .__code__.co_argcount is how many parameters the function has
        # len(.__defaults__) is the amount of optional parameters
        argcount = builtin.__code__.co_argcount - 1  # remove self

        if len(args) > argcount:
            return SLTypeError(
                context,
                f"{name}() given more args than expected",
            )
        elif len(args) < (argcount - len(builtin.__defaults__ or [])):
            return SLTypeError(
                context,
                f"{name}() missing required args",
            )
        else:
            raise e


def create_typeerror(context: Context, name: str | list[str], type_: str | list[str]):
    is_list = type(name) == list
    if is_list:
        name = "' and '".join(name)

    if type(type_) == list:
        type_ = " or ".join(type_)

    return SLTypeError(
        context,
        f"argument{'s' if is_list else ''} '{name}' must be of type {type_}",
    )
