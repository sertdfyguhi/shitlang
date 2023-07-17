from ..error import SLTypeError
from ..context import Context


def create_typeerror(context: Context, name: str | list[str], type_: str | list[str]):
    if is_list := type(name) == list:
        name = "' and '".join(name)

    if type(type_) == list:
        type_ = " or ".join(type_)

    return SLTypeError(
        context,
        f"argument{'s' if is_list else ''} '{name}' must be of type {type_}",
    )
