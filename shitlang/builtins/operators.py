from ..error import SLTypeError


class OperatorBuiltins:
    def not_(self, a: bool):
        return not a

    def and_(self, a, b):
        return a and b

    def or_(self, a, b):
        return a or b

    def equals(self, a, b):
        return a == b

    def greater(self, a: int | float, b: int | float):
        return a > b

    def greater_or_equal(self, a: int | float, b: int | float):
        return a >= b

    def less(self, a: int | float, b: int | float):
        return a < b

    def less_or_equal(self, a: int | float, b: int | float):
        return a <= b

    def add(self, a, b, *c):
        try:
            result = a + b
            for value in c:
                result += value

            return result
        except TypeError:
            return SLTypeError(self.context, "arguments could not be added")

    def sub(self, a, b, *c):
        try:
            result = a - b
            for value in c:
                result -= value

            return result
        except TypeError:
            return SLTypeError(self.context, "arguments could not be subtracted")

    def mul(self, a, b, *c):
        try:
            result = a * b
            for value in c:
                result *= value

            return result
        except TypeError:
            return SLTypeError(self.context, "arguments could not be multiplied")

    def div(self, a, b, *c):
        try:
            result = a / b
            for value in c:
                result /= value

            return result
        except TypeError:
            return SLTypeError(self.context, "arguments could not be divided")

    def mod(self, a: int | float, b: int | float):
        return a % b

    def pow(self, a: int | float, b: int | float):
        return a**b
