import random
import math


Number = int | float

PHI = (1 + 5**0.5) / 2


class MathBuiltins:
    def pi(self):
        return math.pi

    def tau(self):
        return math.tau

    def e(self):
        return math.e

    def phi(self):
        return PHI

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

    def to_rad(self, deg: Number):
        return math.radians(deg)

    def to_deg(self, rad: Number):
        return math.degrees(rad)

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
