from string import digits, ascii_letters
from .token import *
from .error import *

ESCAPES = {
    "n": "\n",
    "r": "\r",
    "t": "\t",
    '"': '"',
    "'": "'",
    "\\": "\\",
}

NUMBER_CHARS = digits + "-."
IDENTIFIER_CHARS = ascii_letters + digits + "_"


class Lexer:
    def __init__(self, code, fn):
        self.fn = fn
        self.code = code
        self.i = -1
        self.next()

    def next(self, change_curr: bool = True):
        self.i += 1
        next_char = self.code[self.i] if self.i < len(self.code) else None

        if change_curr:
            self.curr = next_char
        else:
            self.i -= 1

        return next_char

    def tokenize(self, in_args=False):
        tokens = []

        if in_args:
            nests = 1

        while self.curr:
            if in_args:
                if self.curr == ",":
                    tokens.append(Token(TT_COMMA))
                    self.next()
                elif self.curr == "(":
                    nests += 1
                    self.next()
                elif self.curr == ")":
                    nests -= 1
                    self.next()

            if self.curr in " \t\r\n":
                self.next()
            elif self.curr in "\"'":
                tokens.append(self.string())
            elif self.curr in NUMBER_CHARS:
                tokens.append(self.number())
            elif self.curr in ascii_letters:
                tokens.append(self.func())
            elif self.curr == "<":
                tokens.append(self.array())
            else:
                return SLInvalidCharError(self.fn, f"invalid character '{self.curr}'")

            try:
                if is_SLerr(tokens[-1]):
                    return tokens[-1]
            except IndexError:
                # ignore if last token doesnt exist
                continue

        return tokens

    def string(self):
        """tokenizes a string"""
        quote = self.curr
        string = ""

        self.next()

        while self.curr != quote:
            if self.curr is None:
                return SLSyntaxError(self.fn, "unexpected EOF")

            # is escape
            if self.curr == "\\":
                self.next()

                if self.curr is None:
                    return SLSyntaxError(self.fn, "unexpected EOF")
                elif self.curr not in ESCAPES:
                    return SLSyntaxError(self.fn, f"invalid escape '\\{self.curr}'")

                string += ESCAPES[self.curr]
            else:
                string += self.curr

            self.next()

        self.next()
        return Token(TT_STRING, string)

    def number(self):
        """tokenizes a number"""
        number = ""
        is_float = False

        while self.curr and self.curr in NUMBER_CHARS:
            if self.curr == "-" and len(number) > 0 and number[-1] != "-":
                return SLSyntaxError(self.fn, "unexpected minus sign")

            if self.curr == ".":
                if is_float:
                    return SLSyntaxError(self.fn, "unexpected decimal point")

                is_float = True

            number += self.curr
            self.next()

        return Token(TT_NUMBER, (float if is_float else int)(number))

    def array(self):
        """tokenizes an array"""
        pass

    def func(self):
        """tokenizes a function call"""
        name = ""

        while self.curr and self.curr in IDENTIFIER_CHARS:
            name += self.curr
            self.next()

        if (value := name == "true") or name == "false":
            return Token(TT_BOOL, value)
        elif name == "none":
            return Token(TT_NONE)
        elif self.curr is None:
            return SLSyntaxError(self.fn, "unexpected EOF")

        # function call
        if self.curr == "(":
            args = Lexer(self.code[self.i :], self.fn).tokenize(in_args=True)
            if is_SLerr(args):
                return args

            return Token(TT_FUNC_CALL, [name, args])
        else:
            return SLSyntaxError(self.fn, f"expected function call, got '{self.curr}'")
