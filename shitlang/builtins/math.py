import random
import math


class MathBuiltins:
    def sqrt(self, x: int | float):
        return math.sqrt(x)

    # trigonometry
    def sin(self, x: int | float):
        return math.sin(x)

    def cos(self, x: int | float):
        return math.cos(x)

    def tan(self, x: int | float):
        return math.tan(x)

    def asin(self, x: int | float):
        return math.asin(x)

    def acos(self, x: int | float):
        return math.acos(x)

    def atan(self, x: int | float):
        return math.atan(x)

    # rounding
    def round(self, n: float):
        return round(n)

    def floor(self, n: float):
        return math.floor(n)

    def ceil(self, n: float):
        return math.ceil(n)

    def random(self, seed: int | float | str | None = None):
        random.seed(seed)
        return random.random()
