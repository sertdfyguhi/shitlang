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

    def tokenize(self, mode: str = "", in_lambda: bool = False):
        tokens = []
        comment_char = None

        is_termed = mode in TERMINALS
        if is_termed:
            close_char, sep_char, term_name = TERMINALS[mode]
            res = []
            in_lambda_def = False

        while self.curr:
            if comment_char:
                if (comment_char == ";" and self.curr == "\n") or (
                    comment_char == "=" and self.curr == "="
                ):
                    comment_char = None

                self.next()
                continue

            if is_termed and (self.curr == sep_char or self.curr == close_char):
                if len(tokens) == 0:
                    if self.curr == sep_char:
                        if mode == "pipe":
                            in_lambda = True
                            in_lambda_def = True
                            self.next(error_on_EOF=True)
                            continue
                        else:
                            raise SLSyntaxError(
                                self.context, f"unexpected {sep_char!r}"
                            )
                    elif mode == "pipe":
                        raise SLSyntaxError(self.context, "empty pipe")
                    else:
                        # is close char
                        self.next()
                        break
                elif not in_lambda_def and len(tokens) > 1:
                    raise SLSyntaxError(self.context, f"multiple tokens in {term_name}")
                elif in_lambda_def and self.curr == sep_char:
                    raise SLSyntaxError(
                        self.context, f"unexpected {sep_char!r} in lambda function"
                    )

                if not in_lambda_def:
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
                    if in_lambda_def:
                        self.next()

                        if self.curr and self.curr in digits:
                            arg_num = self.number().value
                            if arg_num <= 0 or type(arg_num) != int:
                                raise SLSyntaxError(
                                    self.context,
                                    "argument number after lambda must be an integer over zero",
                                )
                        else:
                            arg_num = 0

                        res.append(Token(TT_LAMBDA_DEF, [tokens, arg_num]))
                    else:
                        self.next()

                    break

                self.next(error_on_EOF=True)
                continue

            if self.curr in " \t\r\n":
                self.next()
            elif self.curr in ";=":
                comment_char = self.curr
                self.next()
            elif self.curr in "\"'":
                tokens.append(self.string())
                self.next()
            elif self.curr in digits + "-+.":
                tokens.append(self.number())
            elif self.curr in ascii_letters:
                tokens.append(self.func(in_lambda=in_lambda))
            elif self.curr == "<":
                array = self.termed(mode="arr", in_lambda=in_lambda)
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
                self.next()
            elif mode == "args" and self.curr == "_":
                value = "_"

                self.next()

                while self.curr == "_":
                    value += "_"
                    self.next()

                if in_lambda:
                    tokens.append(
                        Token(TT_FUNC_CALL, ["get", [Token(TT_STRING, value)]])
                    )
                else:
                    tokens.append(Token(TT_UNDERSCORE, value))
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
        number_start = self.i
        is_float = False

        while self.curr in "-+":
            self.next(error_on_EOF=True)

        if self.curr not in digits + ".":
            raise SLSyntaxError(self.context, "expected number")

        while self.curr and self.curr in digits + ".":
            if self.curr == ".":
                if is_float:
                    raise SLSyntaxError(self.context, "unexpected decimal point")

                is_float = True

            self.next()

        number_str = self.code[number_start : self.i]
        if number_str == ".":
            raise SLSyntaxError(self.context, "unexpected decimal point")

        return Token(TT_NUMBER, (float if is_float else int)(number_str))

    def termed(self, mode: str = "args", in_lambda: bool = False):
        """tokenizes function arguments (or arrays)"""
        self.next(error_on_EOF=True)

        terms = self.tokenize(mode=mode, in_lambda=in_lambda)
        return terms

    def func(self, in_lambda: bool = False):
        """tokenizes a function call"""
        name_start = self.i

        while self.curr and self.curr in IDENTIFIER_CHARS:
            self.next()

        name = self.code[name_start : self.i]

        if name == "true" or name == "false":
            return Token(TT_BOOL, name == "true")
        elif name == "none":
            return Token(TT_NONE)

        if self.curr is None:
            raise self.EOF_ERR

        # function call
        if self.curr == "(":
            args = self.termed(mode="args", in_lambda=in_lambda)
            return Token(TT_FUNC_CALL, [name, args])
        else:
            raise SLSyntaxError(
                self.context, f"expected function call, got {self.curr!r}"
            )

    def func_def(self):
        """tokenizes a function definition"""
        self.next(error_on_EOF=True)

        name_start = self.i

        while self.curr != "~" and self.curr != "\n":
            self.next(error_on_EOF=True)

        name = self.code[name_start : self.i].strip()
        return Token(TT_FUNC_DEF_END) if name == "" else Token(TT_FUNC_DEF, name)
