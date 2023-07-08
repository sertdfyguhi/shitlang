from ..error import SLTypeError


def create_typeerror(fn: str, name: str | list[str], _type: str | list[str]):
    if n_is_list := type(name) == list:
        name = "' and '".join(name)

    if type(_type) == list:
        _type = " or ".join(_type)

    return SLTypeError(
        fn,
        f"argument{'s' if n_is_list else ''} '{name}' must be of type {_type}",
    )
