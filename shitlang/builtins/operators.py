from .utils import create_typeerror
from ..error import SLTypeError
from ..context import Context


def op_type_check(context: Context, a, b):
    if type(a) not in [int, float] or type(b) not in [int, float]:
        return create_typeerror(context, ["a", "b"], "number")


class OperatorBuiltins:
    def not_(self, a):
        if type(a) != bool:
            return create_typeerror(self.context, "a", "boolean")

        return not a

    def and_(self, a, b):
        if type(a) != bool or type(b) != bool:
            return create_typeerror(self.context, ["a", "b"], "boolean")

        return a and b

    def or_(self, a, b):
        return a or b

    def equals(self, a, b):
        return a == b

    def not_equals(self, a, b):
        return a != b

    def greater(self, a, b):
        if err := op_type_check(self.context, a, b):
            return err

        return a > b

    def greater_or_equal(self, a, b):
        if err := op_type_check(self.context, a, b):
            return err

        return a >= b

    def less(self, a, b):
        if err := op_type_check(self.context, a, b):
            return err

        return a < b

    def less_or_equal(self, a, b):
        if err := op_type_check(self.context, a, b):
            return err

        return a <= b

    def add(self, a, b):
        try:
            return a + b
        except TypeError:
            return SLTypeError(self.context, "arguments 'a' and 'b' cannot be added")

    def subtract(self, a, b):
        if err := op_type_check(self.context, a, b):
            return err

        return a - b

    def multiply(self, a, b):
        if err := op_type_check(self.context, a, b):
            return err

        return a * b

    def divide(self, a, b):
        if err := op_type_check(self.context, a, b):
            return err

        return a / b

    def modulus(self, a, b):
        if err := op_type_check(self.context, a, b):
            return err

        return a % b

    def power(self, a, b):
        if err := op_type_check(self.context, a, b):
            return err

        return a**b
