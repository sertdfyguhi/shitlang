from .utils import create_typeerror


class StringBuiltins:
    def replace(self, pattern, new, string):
        if any(type(x) != str for x in [pattern, new, string]):
            return create_typeerror(
                self.context, ["pattern", "new", "string"], "string"
            )

        return string.replace(pattern, new)

    def split(self, pattern, string):
        if type(pattern) != str or type(string) != str:
            return create_typeerror(self.context, ["pattern", "string"], "string")

        return string.split(pattern)

    def format(self, string, *args):
        if type(string) != str:
            return create_typeerror(self.context, "string", "string")

        return string.format(*args)

    def repeat(self, obj, amount):
        if type(obj) not in [str, list]:
            return create_typeerror(self.context, "obj", ["string", "array"])
        elif type(amount) != int:
            return create_typeerror(self.context, "amount", "integer")

        return obj * amount
