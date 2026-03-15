from ..error import SLTypeError, SLIndexError, SLValueError
from ..function import Function


class ArrayBuiltins:
    def get_index(self, array: list | str, index: int):
        try:
            return array[index]
        except IndexError:
            raise SLIndexError(self.context, "argument 'index' out of range of 'array'")

    def set_index(self, array: list | str, index: int, value):
        if isinstance(array, list):
            array = array.copy()

        try:
            array[index] = value
        except IndexError:
            raise SLIndexError(self.context, "argument 'index' out of range of 'array'")

        return array

    def join(self, array: list[str], sep: str):
        return sep.join(array)

    def remove(self, array: list, index: int):
        temp = array.copy()

        try:
            temp.pop(index)
        except IndexError:
            raise SLIndexError(self.context, "argument 'index' out of range of 'array'")

        return temp

    def append(self, array: list, value, index: int = None):
        temp = array.copy()
        temp.insert(index if index else len(array), value)
        return temp

    def swap(self, array: list, index1: int, index2: int):
        arr = array.copy()

        try:
            arr[index1], arr[index2] = arr[index2], arr[index1]
        except IndexError:
            raise SLIndexError(self.context, "indices out of range of 'array'")

        return arr

    def slice(self, array: list | str, start: int, end: int = None):
        try:
            return array[start:end]
        except IndexError:
            raise SLIndexError(self.context, "indices out of range of 'array'")

    def reverse(self, array: list | str):
        return list(reversed(array))

    def sum(self, array: list[int | float]):
        return sum(array)

    def min(self, array: list[int | float]):
        return min(array)

    def max(self, array: list[int | float]):
        return max(array)

    def length(self, array: list | str):
        return len(array)

    def find(self, array: list | str, value):
        return [i for i, val in enumerate(array) if val == value]

    def find_by(self, array: list, condition: Function, index: bool = False):
        if len(condition.params) != 1:
            raise SLTypeError(
                self.context,
                "argument 'condition' must be a function with one parameter",
            )

        if index:
            return [i for i, value in enumerate(array) if condition.run(value)]
        else:
            return [value for value in array if condition.run(value)]

    def iterate(self, array: list | str, func: Function):
        if len(func.params) != 1:
            raise SLTypeError(
                self.context,
                "argument 'func' must be a function with one parameter",
            )

        for value in array:
            func.run(value)

    def map(self, array: list, func: Function):
        if len(func.params) != 1:
            raise SLTypeError(
                self.context,
                "argument 'func' must be a function with one parameter",
            )

        return list(map(func.run, array))

    def expand(self, array: list, var_names: list[str]):
        if len(var_names) > len(array):
            raise SLValueError(
                self.context, "argument 'var_names' has more values than 'array'"
            )

        for i in range(len(var_names)):
            self.vars.set(var_names[i], array[i])
