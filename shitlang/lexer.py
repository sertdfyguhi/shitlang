from string import digits, ascii_letters
from .token import *
from .error import Error

ESCAPES = {
    'n': '\n',
    'r': '\r',
    't': '\t',
    '"': '"',
    "'": "'",
}

class Lexer:
    def __init__(self, code):
        self.code = code
        self.i = -1
        self.next()

    def next(self):
        self.i += 1
        self.curr = self.code[self.i] if self.i < len(self.code) else None
    
    def tokenize(self, arg=False):
        tokens = []
        in_comment = False

        while self.curr:
            if in_comment:
                if self.curr in '\n-':
                    in_comment = not in_comment
                self.next()
            elif self.curr in ' \t\n':
                self.next()
            elif self.curr in '"\'':
                tokens.append(self.string())
            elif self.curr == '<':
                tokens.append(self.array())
            elif self.curr == '-':
                in_comment = not in_comment
                self.next()
            elif self.curr in digits + '-':
                tokens.append(self.number())
            elif self.curr in ascii_letters:
                tokens.append(self.func_call())
            elif arg and self.curr == ',':
                if tokens[-1].type == TT_COMMA:
                    return Error('SyntaxError', 'unexpected ","')
                tokens.append(Token(TT_COMMA))
                self.next()
            else:
                return Error('InvalidCharError', repr(self.curr))

            if len(tokens) > 0 and not isinstance(tokens[-1], Token):
                return tokens[-1]

        return tokens

    def string(self):
        quote = self.curr
        string = ''

        self.next()

        while self.curr != quote:
            if not self.curr:
                return Error('SyntaxError', 'unexpected EOF')

            if self.curr == '\\':
                if len(string) == 0 or string[-1] != '\\':
                    self.next()

                    if not self.curr:
                        return Error('SyntaxError', 'unexpected EOF')

                    if self.curr not in ESCAPES:
                        return Error('SyntaxError', 'invalid escape character')

                    string += ESCAPES[self.curr]
                    self.next()
                    continue

            string += self.curr
            self.next()

        self.next()

        return Token(TT_STRING, string)

    def number(self):
        number = ''

        while self.curr and self.curr in digits + '.-':
            if self.curr == '-' and number.count('-') != len(number):
                return Error('SyntaxError', 'unexpected "-"')
            number += self.curr
            self.next()

        if '-' in number:
            if number.count('-') % 2 == 0:
                number = number.replace('-', '')
            else:
                number = number.replace('-' * number.count('-'), '-')

        if number.count('.') > 1:
            return Error('SyntaxError', 'unexpected decimal point')

        return Token(
            TT_NUMBER,
            int(number) if number.count('.') == 0 else float(number)
        )

    def array(self):
        array_str = ''
        opens = 1
        in_str = False
        quote = None

        self.next()

        if self.curr == '>': opens -= 1

        while opens > 0:
            if not self.curr:
                return Error('SyntaxError', 'unexpected EOF')   

            if not quote and self.curr in '"\'':
                quote = self.curr

            if self.curr == quote and self.code[self.i-1] != '\\':
                in_str = not in_str
                quote = None

            array_str += self.curr
            self.next()

            if self.curr == '<' and not in_str: opens += 1
            if self.curr == '>' and not in_str: opens -= 1

        self.next()

        array = Lexer(array_str).tokenize(True)

        if isinstance(array, Error): return array

        return Token(TT_ARRAY, array)

    def args(self):
        args = ''
        opens = 1
        in_str = False
        quote = None

        if self.curr == ')': opens -= 1

        while opens > 0:
            if not self.curr:
                return Error('SyntaxError', 'unexpected EOF')   

            if not quote and self.curr in '"\'':
                quote = self.curr

            if self.curr == quote and self.code[self.i-1] != '\\':
                in_str = not in_str
                quote = None

            args += self.curr
            self.next()

            if self.curr == '(' and not in_str: opens += 1
            if self.curr == ')' and not in_str: opens -= 1

        self.next()

        return Lexer(args).tokenize(True)

    def func_call(self):
        name = ''

        while (self.curr != '(' and
            self.curr and
            self.curr in ascii_letters + '_'
        ):
            name += self.curr
            self.next()

            if name in ['True', 'False']:
                return Token(TT_BOOL, True if name == 'True' else False)
            elif name == 'None':
                return Token(TT_NONE)

        if self.curr != '(':
            return Error('SyntaxError', 'expected function to be called')

        self.next()

        args = self.args()

        if isinstance(args, Error): return args

        return Token(TT_FUNC_CALL, [name, args])