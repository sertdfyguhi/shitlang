from ..error import *

from beartype.roar import BeartypeCallHintParamViolation


RESERVED_BUILTINS = [
    "not",
    "and",
    "or",
    "while",
    "if",
    "try",
    "import",
]


def run_builtin(name: str, args: list, builtins):
    builtin = getattr(builtins, name + "_" if name in RESERVED_BUILTINS else name, None)
    if builtin is None:
        raise SLBuiltinError(builtins.context, f"no builtin named '{name}'")

    try:
        return builtin(*args)
    except TypeError as err:
        # TODO: refactor to use inspect.signature or smth
        # .__code__.co_argcount is how many parameters the function has
        # len(.__defaults__) is the amount of optional parameters
        argcount = builtin.__code__.co_argcount - 1  # remove self

        if len(args) > argcount:
            raise SLTypeError(
                builtins.context,
                f"{name}() given {len(args) - argcount} more args than expected",
            )
        elif len(args) < (argcount - len(builtin.__defaults__ or [])):
            raise SLTypeError(
                builtins.context,
                f"{name}() missing required args",
            )
        else:
            raise SLTypeError(builtins.context, str(err))
    except BeartypeCallHintParamViolation as err:
        message = str(err)
        message = message.replace("type hint", "type")
        message = message.replace("Method", "Builtin")
        message = message.replace("shitlang.builtins.", "")
        message = message.replace("list", "array")

        raise SLTypeError(builtins.context, message)
    except RecursionError:
        raise SLRecursionError(builtins.context, "maximum recursion depth exceeded")
    except SLError as err:
        raise err
    except Exception as err:
        raise SLError(type(err).__name__, builtins.context, str(err))
