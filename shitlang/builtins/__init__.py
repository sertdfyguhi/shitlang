from beartype.claw import beartype_this_package

beartype_this_package()

from .operators import OperatorBuiltins
from .variables import VariableBuiltins
from .function import FunctionBuiltins
from .string import StringBuiltins
from .array import ArrayBuiltins
from .types import TypeBuiltins
from .math import MathBuiltins
from .time import TimeBuiltins
from .io import IOBuiltins

from ..environment import Environment
from ..context import Context
from ..vars import Variables


class Builtins(
    OperatorBuiltins,
    VariableBuiltins,
    FunctionBuiltins,
    StringBuiltins,
    ArrayBuiltins,
    TypeBuiltins,
    MathBuiltins,
    TimeBuiltins,
    IOBuiltins,
):
    def __init__(
        self,
        vars_: Variables,
        context: Context,
        environment: Environment,
    ) -> None:
        self.vars = vars_
        self.context = context
        self.environment = environment
