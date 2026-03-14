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

TERMINALS = {
    "args": (")", ",", "arguments"),
    "arr": (">", ",", "array"),
    "pipe": ("]", ">", "pipe"),
}


class Lexer:
    def __init__(self, code: str, context: Context):
        self.context = context
        self.code = code
        self.i = -1

        self.next()

    def next(self, error_on_EOF: bool = False):
        self.i += 1
        self.curr = self.code[self.i] if self.i < len(self.code) else None

        if error_on_EOF and self.curr is None:
            raise SLSyntaxError(self.context, "unexpected EOF")

        return self.curr

    def tokenize(self, mode: str = ""):
        tokens = []
        comment = None

        is_termed = mode in TERMINALS
        if is_termed:
            close_char, sep_char, term_name = TERMINALS[mode]
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
                        raise SLSyntaxError(self.context, "unexpected comma")
                    elif mode == "pipe":
                        raise SLSyntaxError(self.context, "empty pipe")
                    else:
                        break

                if len(tokens) > 1:
                    raise SLSyntaxError(
                        self.context,
                        f"multiple tokens in {term_name}",
                    )

                if mode == "pipe" and len(res) > 0:
                    if tokens[0].type != TT_FUNC_CALL:
                        raise SLSyntaxError(
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
                tokens.append(Token(TT_ARRAY, array))
            elif self.curr == "[":
                piped = self.termed(mode="pipe")
                tokens.append(piped[0])
            elif self.curr == "~":
                if is_termed:
                    raise SLSyntaxError(
                        self.context, f"cannot define function in {term_name}"
                    )

                tokens.append(self.func_def())
            elif mode == "args" and self.curr == "_":
                tokens.append(Token(TT_UNDERSCORE))
                self.next()
            else:
                raise SLInvalidCharError(
                    self.context, f"invalid character {self.curr!r}"
                )

        return res if is_termed else tokens

    def string(self):
        """tokenizes a string"""
        quote = self.curr
        string = ""

        self.next(error_on_EOF=True)

        while self.curr != quote:
            # check if is escape
            if self.curr == "\\":
                self.next(error_on_EOF=True)

                if self.curr not in ESCAPES:
                    raise SLSyntaxError(self.context, f"invalid escape '\\{self.curr}'")

                string += ESCAPES[self.curr]
            else:
                string += self.curr

            self.next(error_on_EOF=True)

        self.next()
        return Token(TT_STRING, string)

    def number(self):
        """tokenizes a number"""
        number = ""
        is_float = False

        while self.curr and self.curr in NUMBER_CHARS:
            if self.curr == "-" and len(number) > 0 and number[-1] != "-":
                raise SLSyntaxError(self.context, "unexpected minus sign")

            if self.curr == ".":
                if is_float:
                    raise SLSyntaxError(self.context, "unexpected decimal point")

                is_float = True

            number += self.curr
            self.next()

        if number == ".":
            raise SLSyntaxError(self.context, "unexpected decimal point")

        return Token(TT_NUMBER, (float if is_float else int)(number))

    def termed(self, mode: str = "args"):
        """tokenizes function arguments (or arrays)"""
        self.next(error_on_EOF=True)

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
            raise self.EOF_ERR

        # function call
        if self.curr == "(":
            args = self.termed(mode="args")
            return Token(TT_FUNC_CALL, [name, args])
        else:
            raise SLSyntaxError(
                self.context, f"expected function call, got {self.curr!r}"
            )

    def func_def(self):
        """tokenizes a function definition"""
        name = ""

        self.next(error_on_EOF=True)

        while self.curr != "~" and self.curr != "\n":
            name += self.curr
            self.next(error_on_EOF=True)

        self.next()
        name = name.strip()
        return Token(TT_FUNC_DEF_END) if name == "" else Token(TT_FUNC_DEF, name)
