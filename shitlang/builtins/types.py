from ..error import SLValueError
from types import NoneType

TYPE_TO_STRING_TABLE = {
    str: "str",
    int: "int",
    float: "float",
    bool: "bool",
    list: "array",
    NoneType: "none",
}


class TypeBuiltins:
    def type(self, value):
        return TYPE_TO_STRING_TABLE[type(value)]

    def to_int(self, value):
        try:
            return int(value)
        except ValueError:
            return SLValueError(self.fn, "argument 'value' cannot be converted to int")

    def to_float(self, value):
        try:
            return float(value)
        except ValueError:
            return SLValueError(
                self.fn, "argument 'value' cannot be converted to float"
            )

    def to_bool(self, value):
        try:
            return bool(value)
        except ValueError:
            return SLValueError(self.fn, "argument 'value' cannot be converted to bool")

    def to_string(self, value):
        return self._print([value])
