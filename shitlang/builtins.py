from .function import Function
from .token import *
from .error import Error
from os.path import exists
import math

class Builtins:
    def __init__(self, vars) -> None:
        self.vars = vars

    def print(self, *data):
        print(self._print(data))

    def _print(self, values, array=False):
        data = values if type(values) == list else list(values)

        for i in range(len(data)):
            if type(data[i]) == list:
                data[i] = f'<{self._print(data[i], True)}>'
            elif type(data[i]) == bool:
                data[i] = 'true' if data[i] else 'false'
            elif data[i] == None:
                data[i] = 'none'
            elif array and type(data[i]) == str:
                data[i] = repr(data[i])
            else:
                data[i] = str(data[i])
        
        return (', ' if array else ' ').join(data)

    def set(self, name, value):
        if type(name) != str: 
            return Error('TypeError', "argument 'name' must be a string")
        return self.vars.set(name, value)

    def get(self, name):
        if type(name) != str: 
            return Error('TypeError', "argument 'name' must be a string")
        return self.vars.get(name)

    def delete(self, name): 
        if type(name) != str: 
            return Error('TypeError', "argument 'name' must be a string")
        return self.vars.delete(name)

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

    def add(self, *numbers):
        if len(numbers) == 0:
            return Error('TypeError', "argument 'numbers' must be an array of numbers that has at least one value")

        try:
            return sum(numbers)
        except TypeError:
            return Error('TypeError', "argument 'numbers' must be an array of numbers that has at least one value")

    def subtract(self, a, b):
        if type(a) not in [int, float] or type(b) not in [int, float]: 
            return Error('TypeError', "arguments 'a' and 'b' must be a number")
        return a - b

    def multiply(self, a, b):
        if type(a) not in [int, float] or type(b) not in [int, float]:
            return Error('TypeError', "argument 'a' and 'b' must be a number")
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
        return math.sqrt(a)

    def chr(self, a):
        if type(a) != int:
            return Error('TypeError', "argument 'a' must be an integer")
        return chr(a)

    def ord(self, a):
        if type(a) != str:
            return Error('TypeError', "argument 'a' must be a string")
        return ord(a)

    def function(self, file, params=[], allow_use_vars=False):
        if type(file) != str:
            return Error('TypeError', "argument 'file' must be a string")
        elif any(type(param) != str for param in params):
            return Error('TypeError', "argument 'params' must be an array of strings")
        elif type(allow_use_vars) != bool:
            return Error('TypeError', "argument 'allow_use_vars' must be a boolean")
        elif not exists(file):
            return Error('FileNotFoundError', f"file {file!r} not found")

        return Function(
            open(file).read(),
            params,
            self.vars,
            allow_use_vars
        )

    def run(self, func, args):
        if not isinstance(func, Function):
            return Error('TypeError', "argument 'func' must be a function")
        elif type(args) != list:
            return Error('TypeError', "argument 'args' must be an array")

        r = func.run(*args)
        if isinstance(r, Error): return r
        return None if type(r) != list else r[0]

    def return_(self, value=None):
        return value

    def replace(self, replace, replacement, string):
        if any(type(x) != str for x in [replace, replacement, string]):
            return Error('TypeError', "arguments 'replace', 'replacement' and 'string' must be a string")
        return string.replace(replace, replacement)

    def format(self, string, *args):
        if type(string) != str:
            return Error('TypeError', "argument 'string' must be a string")
        return string.format(*args)

    def index(self, array, index):
        if type(array) != list:
            return Error('TypeError', "argument 'array' must be an array")
        elif type(index) != int:
            return Error('TypeError', "argument 'index' must be an integer")
        return array[index]

    def join(self, separator, array):
        if type(separator) != str:
            return Error('TypeError', "argument 'separator' must be a string")
        elif type(array) != list or any(type(el) != str for el in array):
            return Error('TypeError', "argument 'array' must be an array of strings")
        return separator.join(array)

    def remove(self, array, index):
        if type(array) != list:
            return Error('TypeError', "argument 'array' must be an array")
        elif type(index) != int:
            return Error('TypeError', "argument 'index' must be an integer")
        temp = array.copy()
        temp.pop(index)
        return temp

    def append(self, array, value, index=None):
        if type(array) != list:
            return Error('TypeError', "argument 'array' must be an array")
        elif index and type(index) != int:
            return Error('TypeError', "argument 'index' must be an integer")
        temp = array.copy()
        temp.insert(index if index else len(array), value)
        return temp

    def reverse(self, a):
        if type(a) not in [list, str]:
            return Error('TypeError', "argument 'a' must be a string or an array")
        return list(reversed(a))

    def split(self, deliminator, string):
        if type(deliminator) != str or type(string) != str:
            return Error('TypeError', "arguments 'deliminator' and 'string' must be a string")
        return string.split(deliminator)

    def while_(self, condition, loop):
        if (not isinstance(condition, Function) or not isinstance(loop, Function) or
            len(condition.params) > 0 or len(loop.params) > 0):
            return Error('TypeError', "arguments 'condition' and 'loop' must be a function with no parameters")

        condition.allow_use_vars = True
        loop.allow_use_vars = True

        c = condition.run()
        if isinstance(c, Error): return c

        while c if type(c) != list else c[0]:
            res = loop.run()

            if isinstance(res, Error): return res
            elif res != None: return [res, 'return']

            c = condition.run()
            if isinstance(c, Error): return c

    def if_(self, condition, func, else_=None):
        if (not isinstance(condition, Function) or
            not isinstance(func, Function) or
            len(condition.params) > 0 or len(func.params) > 0):
            return Error('TypeError', "arguments 'condition' and 'func' must be a function with no parameters")
        elif else_ and (not isinstance(else_, Function) or len(else_.params) > 0):
            return Error('TypeError', "argument 'else' must be a function with no parameters")

        condition.allow_use_vars = True
        func.allow_use_vars = True
        if else_:
            else_.allow_use_vars = True

        c = condition.run()
        if isinstance(c, Error): return c

        res = (func if (None if type(c) != list else c[0]) else else_)
        if res: res = res.run()

        if isinstance(res, Error): return res
        elif res != None: return [res, 'return']

    def min(self, array):
        if type(array) != list or any(type(e) not in [int, float] for e in array):
            return Error('TypeError', "argument 'array' must be an array of numbers")
        return min(array)

    def max(self, array):
        if type(array) != list or any(type(e) not in [int, float] for e in array):
            return Error('TypeError', "argument 'array' must be an array of numbers")
        return max(array)

    def set_index(self, index, value, array):
        if type(index) != int:
            return Error('TypeError', "argument 'index' must be an integer")
        elif type(array) != list:
            return Error('TypeError', "argument 'array' must be an array")
        arr = array.copy()
        arr[index] = value
        return arr

    def swap(self, index1, index2, array):
        if type(index1) != int or type(index2) != int:
            return Error('TypeError', "argument 'index1' and 'index2' must be an integer")
        elif type(array) != list:
            return Error('TypeError', "argument 'array' must be an array")
        arr = array.copy()
        arr[index1], arr[index2] = arr[index2], arr[index1]
        return arr

    def length(self, value):
        if type(value) not in [list, str]:
            return Error('TypeError', "argument 'value' must be an array or string")
        return len(value)

    def slice(self, value, start, end=None):
        if type(value) not in [list, str]:
            return Error('TypeError', "argument 'value' must be an array or string")
        elif type(start) != int or (type(end) != int and end is not None):
            return Error('TypeError', "argument 'start' and 'end' must be an integer")
        return value[start:end]

    def run_builtin(self, name, args):
        if type(name) != str:
            return Error('TypeError', "argument 'name' must be a string")
        elif type(args) != list:
            return Error('TypeError', "argument 'args' must be an array")

        try:
            f = getattr(
                self,
                name,
                lambda *_: Error('BuiltinError', f'no builtin named {name}')
            )
            return f(*args)
        except TypeError:
            if len(args) > (f.__code__.co_argcount - 1):
                return Error('TypeError', f'{name}() given more arguments than expected')
            else:
                return Error('TypeError', f'{name}() missing required arguments')
        except AttributeError:
            return Error('BuiltinError', f'no builtin named {name}')

    def sin(self, x):
        if type(x) not in [int, float]:
            return Error('TypeError', "argument 'x' must be a number")
        return math.sin(x)

    def cos(self, x):
        if type(x) not in [int, float]:
            return Error('TypeError', "argument 'x' must be a number")
        return math.cos(x)

    def tan(self, x):
        if type(x) not in [int, float]:
            return Error('TypeError', "argument 'x' must be a number")
        return math.tan(x)

    def repeat(self, data, factor):
        if type(data) not in [str, list]:
            return Error('TypeError', "argument 'data' must be a string or an array")
        elif type(factor) != int:
            return Error('TypeError', "argument 'factor' must be an int")
        return data * factor