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

        # need self.context
        self.EOF_ERR = SLSyntaxError(self.context, "unexpected EOF")

    def next(self, change_curr: bool = True):
        self.i += 1
        next_char = self.code[self.i] if self.i < len(self.code) else None

        if change_curr:
            self.curr = next_char
        else:
            self.i -= 1

        return next_char

    def tokenize(self, mode: str = ""):
        tokens = []
        comment = None

        terminals = {
            "args": (")", ",", "arguments"),
            "arr": (">", ",", "array"),
            "pipe": ("]", ">", "pipe"),
        }

        is_termed = mode in terminals
        if is_termed:
            close_char, sep_char, term_name = terminals[mode]
            res = []

        while self.curr:
            if comment is not None:
                if (comment == ";" and self.curr == "\n") or (
                    comment == "=" and self.curr == "="
                ):
                    comment = None

                self.next()
                continue

            if is_termed and (self.curr == sep_char or self.curr == close_char):
                if len(tokens) == 0:
                    if self.curr == sep_char:
                        return SLSyntaxError(self.context, "unexpected comma")
                    elif mode == "pipe":
                        return SLSyntaxError(self.context, "empty pipe")
                    else:
                        break

                if len(tokens) > 1:
                    return SLSyntaxError(
                        self.context,
                        f"multiple tokens in {term_name}",
                    )

                if mode == "pipe" and len(res) > 0:
                    if tokens[0].type != TT_FUNC_CALL:
                        return SLSyntaxError(
                            self.context,
                            f"expected function call in pipe, found {tokens[0].type}",
                        )

                    has_underscore = False
                    args = tokens[0].value[1]

                    for i, arg in enumerate(args):
                        if arg.type == TT_UNDERSCORE:
                            args[i] = res[0]
                            has_underscore = True

                    if not has_underscore:
                        args.append(res[0])

                    res[0] = tokens[0]
                else:
                    res.append(tokens[0])

                tokens = []

                if self.curr == close_char:
                    break
                else:
                    self.next()
                    continue

            if self.curr in " \t\r\n":
                self.next()
                continue
            elif self.curr in ";=":
                comment = self.curr
                self.next()
                continue
            elif self.curr in "\"'":
                tokens.append(self.string())
            elif self.curr in NUMBER_CHARS:
                tokens.append(self.number())
            elif self.curr in ascii_letters:
                tokens.append(self.func())
            elif self.curr == "<":
                array = self.termed(mode="arr")
                if is_SLerr(array):
                    return array

                tokens.append(Token(TT_ARRAY, array))
            elif self.curr == "[":
                piped = self.termed(mode="pipe")
                if is_SLerr(piped):
                    return piped

                tokens.append(piped[0])
            elif self.curr == "~":
                if is_termed:
                    return SLSyntaxError(
                        self.context, f"cannot define function in {term_name}"
                    )

                tokens.append(self.func_def())
            elif mode == "args" and self.curr == "_":
                self.next()
                tokens.append(Token(TT_UNDERSCORE))
            else:
                return SLInvalidCharError(
                    self.context, f"invalid character {self.curr!r}"
                )

            if len(tokens) > 0 and is_SLerr(tokens[-1]):
                return tokens[-1]

        return res if is_termed else tokens

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

    def termed(self, mode: str = "args"):
        """tokenizes function arguments (or arrays)"""
        self.next()
        if self.curr is None:
            return self.EOF_ERR

        terms = self.tokenize(mode=mode)
        self.next()
        return terms

    def func(self):
        """tokenizes a function call"""
        name = ""

        while self.curr and self.curr in IDENTIFIER_CHARS:
            name += self.curr
            self.next()

        if name == "true" or name == "false":
            return Token(TT_BOOL, name == "true")
        elif name == "none":
            return Token(TT_NONE)

        if self.curr is None:
            return self.EOF_ERR

        # function call
        if self.curr == "(":
            args = self.termed(mode="args")
            if is_SLerr(args):
                return args

            return Token(TT_FUNC_CALL, [name, args])
        else:
            return SLSyntaxError(
                self.context, f"expected function call, got '{self.curr}'"
            )

    def func_def(self):
        """tokenizes a function definition"""
        name = ""

        self.next()

        while self.curr != "~" and self.curr != "\n":
            if self.curr is None:
                return self.EOF_ERR

            name += self.curr
            self.next()

        self.next()

        name = name.strip()

        return Token(TT_FUNC_DEF_END) if name == "" else Token(TT_FUNC_DEF, name)
