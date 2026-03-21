import random
import math


Number = int | float


class MathBuiltins:
    def sqrt(self, x: Number):
        return math.sqrt(x)

    # trigonometry
    def sin(self, x: Number):
        return math.sin(x)

    def cos(self, x: Number):
        return math.cos(x)

    def tan(self, x: Number):
        return math.tan(x)

    def asin(self, x: Number):
        return math.asin(x)

    def acos(self, x: Number):
        return math.acos(x)

    def atan(self, x: Number):
        return math.atan(x)

    # rounding
    def round(self, n: float):
        return round(n)

    def floor(self, n: float):
        return math.floor(n)

    def ceil(self, n: float):
        return math.ceil(n)

    def random(self, seed: Number | str | None = None):
        random.seed(seed)
        return random.random()
