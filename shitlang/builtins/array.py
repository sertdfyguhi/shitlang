from ..error import SLTypeError, SLIndexError
from .utils import create_typeerror
from ..function import Function


class ArrayBuiltins:
    def get_index(self, array, index):
        if type(array) not in [list, str]:
            return create_typeerror(self.context, "array", ["array", "string"])
        elif type(index) != int:
            return create_typeerror(self.context, "index", "integer")

        try:
            return array[index]
        except IndexError:
            return SLIndexError(
                self.context, "argument 'index' out of range of 'array'"
            )

    def set_index(self, array, index, value):
        if type(array) not in [list, str]:
            return create_typeerror(self.context, "array", ["array", "string"])
        elif type(index) != int:
            return create_typeerror(self.context, "index", "integer")

        if type(array) == list:
            array = array.copy()

        try:
            array[index] = value
        except IndexError:
            return SLIndexError(
                self.context, "argument 'index' out of range of 'array'"
            )

        return array

    def join(self, array, sep):
        if type(array) != list or any(type(value) != str for value in array):
            return create_typeerror(self.context, "array", "array of strings")
        elif type(sep) != str:
            return create_typeerror(self.context, "sep", "string")

        return sep.join(array)

    def remove(self, array, index):
        if type(array) != list:
            return create_typeerror(self.context, "array", "array")
        elif type(index) != int:
            return create_typeerror(self.context, "index", "integer")

        temp = array.copy()

        try:
            temp.pop(index)
        except IndexError:
            return SLIndexError(
                self.context, "argument 'index' out of range of 'array'"
            )

        return temp

    def append(self, array, value, index=None):
        if type(array) != list:
            return create_typeerror(self.context, "array", "array")
        elif index and type(index) != int:
            return create_typeerror(self.context, "index", "integer")

        temp = array.copy()
        temp.insert(index if index else len(array), value)
        return temp

    def swap(self, array, index1, index2):
        if type(index1) != int or type(index2) != int:
            return create_typeerror(self.context, ["index1", "index2"], "integer")
        elif type(array) != list:
            return create_typeerror(self.context, "array", "array")

        arr = array.copy()

        try:
            arr[index1], arr[index2] = arr[index2], arr[index1]
        except IndexError:
            return SLIndexError(self.context, "indices out of range of 'array'")

        return arr

    def slice(self, value, start, end=None):
        if type(value) not in [list, str]:
            return create_typeerror(self.context, "value", ["array", "string"])
        elif type(start) != int:
            return create_typeerror(self.context, "start", "integer")
        elif end is not None or type(end) != int:
            return create_typeerror(self.context, "end", "integer")

        try:
            return value[start:end]
        except IndexError:
            return SLIndexError(self.context, "indices out of range of 'array'")

    def reverse(self, a):
        if type(a) not in [list, str]:
            return create_typeerror(self.context, "a", ["string", "array"])

        return list(reversed(a))

    def sum(self, array):
        if type(array) != list or any(type(e) not in [int, float] for e in array):
            return create_typeerror(self.context, "array", "array of numbers")

        return sum(array)

    def min(self, array):
        if type(array) != list or any(type(e) not in [int, float] for e in array):
            return create_typeerror(self.context, "array", "array of numbers")

        return min(array)

    def max(self, array):
        if type(array) != list or any(type(e) not in [int, float] for e in array):
            return create_typeerror(self.context, "array", "array of numbers")

        return max(array)

    def length(self, array):
        if type(array) not in [list, str]:
            return create_typeerror(self.context, "array", ["array", "string"])

        return len(array)

    def find(self, array, value):
        if type(array) not in [list, str]:
            return create_typeerror(self.context, "array", ["array", "string"])
        elif type(array) == str and type(value) != str:
            return create_typeerror(self.context, "value", "string")

        return [i for i, val in enumerate(array) if val == value]

    def find_by(self, array, condition, index=False):
        if type(array) != list:
            return create_typeerror(self.context, "array", "array")
        elif not isinstance(condition, Function):
            return create_typeerror(self.context, "condition", "function")
        elif len(condition.params) != 1:
            return SLTypeError(
                self.context,
                "argument 'condition' must be a function with one parameter",
            )
        elif type(index) != bool:
            return create_typeerror(self.context, "index", "boolean")

        if index:
            return [i for i, value in enumerate(array) if condition.run(value)]
        else:
            return [value for value in array if condition.run(value)]

    def iterate(self, array, func):
        if type(array) not in [list, str]:
            return create_typeerror(self.context, "array", ["array", "string"])
        elif not isinstance(func, Function):
            return create_typeerror(self.context, "func", "function")
        elif len(func.params) != 1:
            return SLTypeError(
                self.context,
                "argument 'func' must be a function with one parameter",
            )

        for value in array:
            func.run(value)
