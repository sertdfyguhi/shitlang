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
        # .__code__.co_argcount is how many parameters the function has
        # len(.__defaults__) is the amount of optional parameters
        # wrapped with beartype
        num_args = builtin.__wrapped__.__code__.co_argcount - 1  # remove self
        num_required_args = num_args - len(builtin.__wrapped__.__defaults__ or [])

        if len(args) > num_args:
            raise SLTypeError(
                builtins.context,
                f"given {len(args) - num_args} more arguments than expected",
            )
        elif len(args) < num_required_args:
            raise SLTypeError(
                builtins.context,
                f"missing {num_required_args - len(args)} required arguments",
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
