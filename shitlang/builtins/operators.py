from functools import reduce
import operator


Number = int | float


class OperatorBuiltins:
    def not_(self, a: bool):
        return not a

    def and_(self, a, b):
        return a and b

    def or_(self, a, b):
        return a or b

    def equals(self, a, b):
        return a == b

    def greater(self, a: Number, b: Number):
        return a > b

    def ge(self, a: Number, b: Number):
        return a >= b

    def less(self, a: Number, b: Number):
        return a < b

    def le(self, a: Number, b: Number):
        return a <= b

    def add(self, a: Number | str, b: Number | str, *c: Number | str):
        return reduce(operator.add, [a, b, *c])

    def sub(self, a: Number, b: Number, *c: Number):
        return reduce(operator.sub, [a, b, *c])

    def mul(self, a: Number, b: Number, *c: Number):
        return reduce(operator.mul, [a, b, *c])

    def div(self, a: Number, b: Number, *c: Number):
        return reduce(operator.div, [a, b, *c])

    def mod(self, a: Number, b: Number):
        return a % b

    def pow(self, a: Number, b: Number):
        return a**b
