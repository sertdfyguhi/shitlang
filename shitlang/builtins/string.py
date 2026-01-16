from .utils import create_typeerror
import base64


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

    def concat(self, *strings):
        if any(type(string) != str for string in strings):
            return create_typeerror(self.context, "strings", "string")

        return "".join(strings)

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
