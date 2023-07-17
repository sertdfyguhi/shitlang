from .operators import OperatorBuiltins
from .variables import VariableBuiltins
from .function import FunctionBuiltins
from .string import StringBuiltins
from .array import ArrayBuiltins
from .types import TypeBuiltins
from .math import MathBuiltins
from .io import IOBuiltins

from .utils import create_typeerror
from ..context import Context
from ..vars import Variables

import base64
import random


class Builtins(
    OperatorBuiltins,
    VariableBuiltins,
    FunctionBuiltins,
    StringBuiltins,
    ArrayBuiltins,
    TypeBuiltins,
    MathBuiltins,
    IOBuiltins,
):
    def __init__(self, vars_: Variables, context: Context) -> None:
        self.context = context
        self.vars = vars_

    def random(self, seed=None):
        if seed and type(seed) not in [int, float, str]:
            return create_typeerror(self.context, "seed", ["int", "float", "string"])

        random.seed(seed)
        return random.random()

    def chr(self, a):
        if type(a) != int:
            return create_typeerror(self.context, "a", "integer")

        return chr(a)

    def ord(self, a):
        if type(a) != str:
            return create_typeerror(self.context, "a", "string")

        return ord(a)

    def encode_base64(self, string):
        if type(string) != str:
            return create_typeerror(self.context, "string", "string")

        return base64.b64encode(string.encode("ascii")).decode("ascii")

    def decode_base64(self, string):
        if type(string) != str:
            return create_typeerror(self.context, "string", "string")

        return base64.b64decode(string.encode("ascii")).decode("ascii")
