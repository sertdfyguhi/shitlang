import base64


class StringBuiltins:
    def replace(self, pattern: str, new: str, string: str):
        return string.replace(pattern, new)

    def split(self, pattern: str, string: str):
        return string.split(pattern)

    def concat(self, *strings: str):
        return "".join(strings)

    def format(self, string: str, *args):
        return string.format(*args)

    def repeat(self, value: str | list, amount: int):
        return value * amount

    def chr(self, index: int):
        return chr(index)

    def ord(self, char: str):
        return ord(char)

    def encode_base64(self, string: str):
        return base64.b64encode(string.encode("ascii")).decode("ascii")

    def decode_base64(self, string: str):
        return base64.b64decode(string.encode("ascii")).decode("ascii")
