from .utils import create_typeerror
import math


class MathBuiltins:
    def sqrt(self, a):
        if type(a) not in [int, float]:
            return create_typeerror(self.context, "a", "number")

        return math.sqrt(a)

    # trigonometry
    def sin(self, x):
        if type(x) not in [int, float]:
            return create_typeerror(self.context, "x", "number")

        return math.sin(x)

    def cos(self, x):
        if type(x) not in [int, float]:
            return create_typeerror(self.context, "x", "number")

        return math.cos(x)

    def tan(self, x):
        if type(x) not in [int, float]:
            return create_typeerror(self.context, "x", "number")

        return math.tan(x)

    def asin(self, x):
        if type(x) not in [int, float]:
            return create_typeerror(self.context, "x", "number")

        return math.asin(x)

    def acos(self, x):
        if type(x) not in [int, float]:
            return create_typeerror(self.context, "x", "number")

        return math.acos(x)

    def atan(self, x):
        if type(x) not in [int, float]:
            return create_typeerror(self.context, "x", "number")

        return math.atan(x)

    # rounding
    def round(self, n):
        if type(n) != float:
            return create_typeerror(self.context, "n", "float")

        return round(n)

    def floor(self, n):
        if type(n) != float:
            return create_typeerror(self.context, "n", "float")

        return math.floor(n)

    def ceil(self, n):
        if type(n) != float:
            return create_typeerror(self.context, "n", "float")

        return math.ceil(n)
