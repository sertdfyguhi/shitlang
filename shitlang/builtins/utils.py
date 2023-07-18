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

    try:
        builtin = getattr(
            builtins,
            name + "_" if name in RESERVED_BUILTINS else name,
        )

        return builtin(*args)
    except AttributeError as e:
        return SLBuiltinError(context, f"no builtin named '{name}'")
    except TypeError as e:
        # TODO: refactor to use inspect.signature or smth
        # .__code__.co_argcount is how many parameters the function has
        # len(.__defaults__) is the amount of optional parameters
        if len(args) > (builtin.__code__.co_argcount - 1):
            return SLTypeError(
                context,
                f"{name}() given more args than expected",
            )
        elif len(args) < (
            builtin.__code__.co_argcount - len(builtin.__defaults__ or [0])
        ):
            return SLTypeError(
                context,
                f"{name}() missing required args",
            )
        else:
            raise e


def create_typeerror(context: Context, name: str | list[str], type_: str | list[str]):
    if is_list := type(name) == list:
        name = "' and '".join(name)

    if type(type_) == list:
        type_ = " or ".join(type_)

    return SLTypeError(
        context,
        f"argument{'s' if is_list else ''} '{name}' must be of type {type_}",
    )
