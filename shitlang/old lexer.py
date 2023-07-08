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

    def tokenize(self, arg=False):
        tokens = []
        comment = None

        while self.curr:
            if comment:
                if (comment == ";" and self.curr == "\n") or (
                    comment == "-" and self.curr == "-"
                ):
                    comment = None

                self.next()
            elif self.curr in " \t\n":
                self.next()
            elif self.curr in "\"'":
                tokens.append(self.string())
            elif self.curr == "<":
                tokens.append(self.array())
            elif self.curr == "-":
                # TODO: "--comment" wouldnt work
                if self.next(change_curr=False) in digits + "-.":
                    tokens.append(self.number())
                else:
                    comment = "-"
                    self.next()
            elif self.curr == ";":
                comment = ";"
                self.next()
            elif self.curr in ascii_letters:
                tokens.append(self.func_call())
            elif arg and self.curr == ",":
                if len(tokens) == 0 or tokens[-1].type == TT_COMMA:
                    return SLSyntaxError(self.fn, 'unexpected ","')
                elif len(tokens) > 1 and tokens[-2].type != TT_COMMA:
                    return SLSyntaxError(self.fn, 'expected ","')

                tokens.append(Token(TT_COMMA))
                self.next()
            else:
                return SLInvalidCharError(self.fn, repr(self.curr))

            if len(tokens) > 0 and not isinstance(tokens[-1], Token):
                return tokens[-1]

        if arg and len(tokens) > 0 and tokens[-1].type == TT_COMMA:
            return SLSyntaxError(self.fn, 'unexpected ","')
        elif arg and len(tokens) > 1 and tokens[-2].type != TT_COMMA:
            return SLSyntaxError(self.fn, 'expected ","')

        return tokens

    def string(self):
        quote = self.curr
        string = ""

        self.next()

        while self.curr != quote:
            if not self.curr:
                return SLSyntaxError(self.fn, "unexpected EOF")

            if self.curr == "\\":
                self.next()
                if not self.curr:
                    return SLSyntaxError(self.fn, "unexpected EOF")

                if self.curr not in ESCAPES:
                    return SLSyntaxError(self.fn, f"invalid escape '\\{self.curr}'")

                string += ESCAPES[self.curr]
            else:
                string += self.curr

            self.next()

        self.next()

        return Token(TT_STRING, string)

    def array(self):
        array_str = ""
        brackets = 1
        in_str = False
        quote = None

        self.next()

        if self.curr == ">":
            brackets -= 1

        while brackets > 0:
            if not self.curr:
                return SLSyntaxError(self.fn, "unexpected EOF")

            if self.curr == quote and self.code[self.i - 1] != "\\":
                in_str = not in_str
                quote = self.curr if not quote and self.curr in "\"'" else None

            if self.curr == "<" and not in_str:
                brackets += 1

            array_str += self.curr
            self.next()

            if self.curr == ">" and not in_str:
                brackets -= 1

        self.next()

        array = Lexer(array_str, self.fn).tokenize(True)
        if is_SLerr(array):
            return array

        return Token(TT_ARRAY, array)

    def args(self):
        args = ""
        brackets = 1
        in_str = False
        quote = None
        comment = None

        if self.curr == ")":
            brackets -= 1

        while brackets > 0:
            if not self.curr:
                return SLSyntaxError(self.fn, "unexpected EOF")

            if not in_str and not comment and self.curr in "-;":
                comment = self.curr
            elif comment:
                if (comment == ";" and self.curr == "\n") or (
                    comment == "-" and self.curr == "-"
                ):
                    comment = None
                    self.next()
                    if not comment and self.curr == ")" and not in_str:
                        brackets -= 1
                    continue

            if not comment:
                if (
                    self.curr == quote and self.code[self.i - 1] != "\\"
                ) or self.curr in "\"'":
                    in_str = not in_str
                    quote = self.curr if not quote and self.curr in "\"'" else None

                if self.curr == "(" and not in_str:
                    brackets += 1

                args += self.curr

            self.next()

            if not comment and self.curr == ")" and not in_str:
                brackets -= 1

        self.next()

        return Lexer(args, self.fn).tokenize(True)

    def func_call(self):
        name = ""

        while self.curr != "(" and self.curr and self.curr in ascii_letters + "_":
            name += self.curr
            self.next()

            if name in ["true", "false"]:
                return Token(TT_BOOL, True if name == "true" else False)
            elif name == "none":
                return Token(TT_NONE)

        if self.curr != "(":
            return SLSyntaxError(self.fn, "expected function to be called")

        self.next()

        args = self.args()
        print(args)
        if is_SLerr(args):
            return args

        return Token(TT_FUNC_CALL, [name, args])
