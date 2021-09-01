from .vars import Variables
from .function import Function
from .token import *
from .error import Error
from math import sqrt

class Builtins:
    def __init__(self, vars) -> None:
        self.vars = vars

    def print(self, *args):
        print(*args)

    def set(self, key, value):
        if type(key) != str: 
            return Error('TypeError', "argument 'key' must be a string")
        return self.vars.set(key, value)

    def get(self, key):
        if type(key) != str: 
            return Error('TypeError', "argument 'key' must be a string")
        return self.vars.get(key)

    def delete(self, key): 
        if type(key) != str: 
            return Error('TypeError', "argument 'key' must be a string")
        return self.vars.delete(key)

    def input(self, prompt):
        if type(prompt) != str: 
            return Error('TypeError', "argument 'prompt' must be a string")
        return input(prompt)

    def not_(self, a):
        if type(a) != bool:
            return Error('TypeError', "argument 'a' must be a boolean")
        return not a

    def and_(self, a, b):
        if type(a) != bool or type(b) != bool:
            return Error('TypeError', "arguments 'a' and 'b' must be a boolean")
        return a and b

    def or_(self, a, b):
        return a or b

    def equals(self, a, b):
        return a == b

    def not_equals(self, a, b):
        return a != b

    def greater(self, a, b):
        if type(a) not in [int, float] or type(b) not in [int, float]: 
            return Error('TypeError', "arguments 'a' and 'b' must be a number")
        return a > b

    def greater_or_equal(self, a, b):
        if type(a) not in [int, float] or type(b) not in [int, float]: 
            return Error('TypeError', "arguments 'a' and 'b' must be a number")
        return a >= b

    def less(self, a, b):
        if type(a) not in [int, float] or type(b) not in [int, float]: 
            return Error('TypeError', "arguments 'a' and 'b' must be a number")
        return a < b

    def less_or_equal(self, a, b):
        if type(a) not in [int, float] or type(b) not in [int, float]: 
            return Error('TypeError', "arguments 'a' and 'b' must be a number")
        return a <= b

    def add(self, a, b):
        try:
            return a + b
        except TypeError:
            return Error('TypeError', "arguments 'a' and 'b' cannot be added")

    def subtract(self, a, b):
        if type(a) not in [int, float] or type(b) not in [int, float]: 
            return Error('TypeError', "arguments 'a' and 'b' must be a number")
        return a - b

    def multiply(self, a, b):
        if type(b) == str:
            return Error('TypeError', "argument 'b' must not be a string")
        return a * b

    def divide(self, a, b):
        if type(a) not in [int, float] or type(b) not in [int, float]: 
            return Error('TypeError', "arguments 'a' and 'b' must be a number")
        return a / b

    def modulus(self, a, b):
        if type(a) not in [int, float] or type(b) not in [int, float]: 
            return Error('TypeError', "arguments 'a' and 'b' must be a number")
        return a % b

    def power(self, a, b):
        if type(a) not in [int, float] or type(b) not in [int, float]: 
            return Error('TypeError', "arguments 'a' and 'b' must be a number")
        return a ** b

    def sqrt(self, a):
        if type(a) not in [int, float]: 
            return Error('TypeError', "argument 'a' must be a number")
        return sqrt(a)

    def chr(self, a):
        if type(a) != int:
            return Error('TypeError', "argument 'a' must be an integer")
        return chr(a)

    def ord(self, a):
        if type(a) != str:
            return Error('TypeError', "argument 'a' must be a string")
        return ord(a)

    def function(self, file, params=[], allow_use_vars=False):
        return Function(
            open(file).read(),
            params,
            Variables() if not allow_use_vars else self.vars,
            allow_use_vars
        )

    def run(self, func, *args):
        if not isinstance(func, Function):
            return Error('TypeError', "argument 'func' must be a function")
        try:
            return func.run(*args)
        except RecursionError:
            return Error('RecursionError', 'maximum recursion depth exceeded')

    def return_(self, value):
        return value

    def replace(self, a, replace, string):
        if any(type(x) != str for x in [a, replace, string]):
            return Error('TypeError', "arguments 'a', 'replace' and 'string' must be a string")
        return string.replace(a, replace)

    def format(self, string, *args):
        if type(string) != str:
            return Error('TypeError', "argument 'string' must be a string")
        return string.format(*args)