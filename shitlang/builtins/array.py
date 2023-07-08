from .utils import create_typeerror


class ArrayBuiltins:
    def index(self, array, index):
        if type(array) != list:
            return create_typeerror(self.fn, "array", "array")
        elif type(index) != int:
            return create_typeerror(self.fn, "index", "integer")

        return array[index]

    def set_index(self, array, index, value):
        if type(array) != list:
            return create_typeerror(self.fn, "array", "array")
        elif type(index) != int:
            return create_typeerror(self.fn, "index", "integer")

        arr = array.copy()
        arr[index] = value
        return arr

    def join(self, sep, array):
        if type(sep) != str:
            return create_typeerror(self.fn, "sep", "string")
        elif type(array) != list or any(type(el) != str for el in array):
            return create_typeerror(self.fn, "array", "array of strings")

        return sep.join(array)

    def remove(self, array, index):
        if type(array) != list:
            return create_typeerror(self.fn, "array", "array")
        elif type(index) != int:
            return create_typeerror(self.fn, "index", "integer")

        temp = array.copy()
        temp.pop(index)
        return temp

    def append(self, array, value, index=None):
        if type(array) != list:
            return create_typeerror(self.fn, "array", "array")
        elif index and type(index) != int:
            return create_typeerror(self.fn, "index", "integer")

        temp = array.copy()
        temp.insert(index if index else len(array), value)
        return temp

    def swap(self, array, index1, index2):
        if type(index1) != int or type(index2) != int:
            return create_typeerror(self.fn, ["index1", "index2"], "integer")
        elif type(array) != list:
            return create_typeerror(self.fn, "array", "array")

        arr = array.copy()
        arr[index1], arr[index2] = arr[index2], arr[index1]
        return arr

    def slice(self, value, start, end=None):
        if type(value) not in [list, str]:
            return create_typeerror(self.fn, "value", ["array", "string"])
        elif type(start) != int:
            return create_typeerror(self.fn, "start", "integer")
        elif end is not None or type(end) != int:
            return create_typeerror(self.fn, "end", "integer")

        return value[start:end]

    def reverse(self, a):
        if type(a) not in [list, str]:
            return create_typeerror(self.fn, "a", ["string", "array"])

        return list(reversed(a))

    def sum(self, array):
        if type(array) != list or any(type(e) not in [int, float] for e in array):
            return create_typeerror(self.fn, "array", "array of numbers")
        return sum(array)

    def min(self, array):
        if type(array) != list or any(type(e) not in [int, float] for e in array):
            return create_typeerror(self.fn, "array", "array of numbers")

        return min(array)

    def max(self, array):
        if type(array) != list or any(type(e) not in [int, float] for e in array):
            return create_typeerror(self.fn, "array", "array of numbers")

        return max(array)

    def length(self, value):
        if type(value) not in [list, str]:
            return create_typeerror(self.fn, "value", ["array", "string"])

        return len(value)
