from .utils import create_typeerror
from ..error import SLTypeError


def op_type_check(fn: str, a, b):
    if type(a) not in [int, float] or type(b) not in [int, float]:
        return create_typeerror(fn, ["a", "b"], "number")


class OperatorBuiltins:
    def not_(self, a):
        if type(a) != bool:
            return create_typeerror(self.fn, "a", "boolean")

        return not a

    def and_(self, a, b):
        if type(a) != bool or type(b) != bool:
            return create_typeerror(self.fn, ["a", "b"], "boolean")

        return a and b

    def or_(self, a, b):
        return a or b

    def equals(self, a, b):
        return a == b

    def not_equals(self, a, b):
        return a != b

    def greater(self, a, b):
        return a > b if not (err := op_type_check(self.fn, a, b)) else err

    def greater_or_equal(self, a, b):
        return a >= b if not (err := op_type_check(self.fn, a, b)) else err

    def less(self, a, b):
        return a < b if not (err := op_type_check(self.fn, a, b)) else err

    def less_or_equal(self, a, b):
        return a <= b if not (err := op_type_check(self.fn, a, b)) else err

    def add(self, a, b):
        try:
            return a + b
        except TypeError:
            return SLTypeError(self.fn, "arguments 'a' and 'b' cannot be added")

    def subtract(self, a, b):
        return a - b if not (err := op_type_check(self.fn, a, b)) else err

    def multiply(self, a, b):
        return a * b if not (err := op_type_check(self.fn, a, b)) else err

    def divide(self, a, b):
        return a / b if not (err := op_type_check(self.fn, a, b)) else err

    def modulus(self, a, b):
        return a % b if not (err := op_type_check(self.fn, a, b)) else err

    def power(self, a, b):
        return a ** b if not (err := op_type_check(self.fn, a, b)) else err
