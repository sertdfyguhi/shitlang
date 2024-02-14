from string import digits, ascii_letters
from .context import Context
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
    def __init__(self, code: str, context: Context):
        self.context = context
        self.code = code
        self.i = -1

        self.next()

        self.EOF_ERR = SLSyntaxError(self.context, "unexpected EOF")

    def next(self, change_curr: bool = True):
        self.i += 1
        next_char = self.code[self.i] if self.i < len(self.code) else None

        if change_curr:
            self.curr = next_char
        else:
            self.i -= 1

        return next_char

    def tokenize(self, in_args: bool = False, in_arr: bool = False):
        tokens = []

        if in_args or in_arr:
            CLOSE_PAREN = ")" if in_args else ">"
            res = []

        while self.curr:
            if in_args or in_arr:
                if self.curr == ",":
                    if len(tokens) > 1:
                        return SLSyntaxError(
                            self.context, f"multiple tokens in array value"
                        )
                    elif len(tokens) == 0:
                        return SLSyntaxError(self.context, "unexpected comma")

                    res.append(tokens[0])
                    tokens = []

                    self.next()
                    continue
                elif self.curr == CLOSE_PAREN:
                    break

            if self.curr in " \t\r\n":
                self.next()
            elif self.curr in "\"'":
                tokens.append(self.string())
            elif self.curr in NUMBER_CHARS:
                tokens.append(self.number())
            elif self.curr in ascii_letters:
                tokens.append(self.func())
            elif self.curr == "<":
                array = self.args(in_args=False)
                if is_SLerr(array):
                    return array

                tokens.append(Token(TT_ARRAY, array))
            else:
                return SLInvalidCharError(
                    self.context, f"invalid character {self.curr!r}"
                )

            try:
                if is_SLerr(tokens[-1]):
                    return tokens[-1]
            except IndexError:
                # ignore if last token doesnt exist
                continue

        if in_args or in_arr:
            if self.curr != CLOSE_PAREN:
                return self.EOF_ERR

            if len(tokens) == 1:
                res.append(tokens[0])
            elif len(tokens) > 1:
                return SLSyntaxError(self.context, f"multiple tokens in array value")

            return res
        else:
            return tokens

    def string(self):
        """tokenizes a string"""
        quote = self.curr
        string = ""

        self.next()

        while self.curr != quote:
            if self.curr is None:
                return self.EOF_ERR

            # check if is escape
            if self.curr == "\\":
                self.next()
                if self.curr is None:
                    return self.EOF_ERR

                if self.curr not in ESCAPES:
                    return SLSyntaxError(
                        self.context, f"invalid escape '\\{self.curr}'"
                    )

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
            try:
                if self.curr == "-" and number[-1] != "-":
                    return SLSyntaxError(self.context, "unexpected minus sign")
            except IndexError:
                # ignore index error when number is empty
                pass

            if self.curr == ".":
                if is_float:
                    return SLSyntaxError(self.context, "unexpected decimal point")

                is_float = True

            number += self.curr
            self.next()

        return Token(TT_NUMBER, (float if is_float else int)(number))

    def args(self, in_args: bool = True):
        """tokenizes function arguments (or arrays)"""
        self.next()
        if self.curr is None:
            return self.EOF_ERR

        lexer = Lexer(self.code[self.i :], self.context)

        if in_args:
            args = lexer.tokenize(in_args=True)
        else:
            args = lexer.tokenize(in_arr=True)

        if is_SLerr(args):
            return args

        # update lexer position
        lexer.next()
        self.i += lexer.i
        self.curr = lexer.curr

        return args

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

        if self.curr is None:
            return self.EOF_ERR

        # function call
        if self.curr == "(":
            args = self.args()
            if is_SLerr(args):
                return args

            return Token(TT_FUNC_CALL, [name, args])
        else:
            return SLSyntaxError(
                self.context, f"expected function call, got '{self.curr}'"
            )
