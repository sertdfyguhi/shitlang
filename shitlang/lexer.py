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
        comment = ''

        while self.curr:
            if comment:
                if (
                    comment == ';' and self.curr == '\n'
                ) or (
                    comment == '-' and self.curr == '-'
                ): 
                    comment = None
                self.next()
            elif self.curr in ' \t\n':
                self.next()
            elif self.curr in '"\'':
                tokens.append(self.string())
            elif self.curr == '<':
                tokens.append(self.array())
            elif self.curr in '-;':
                comment = self.curr
                self.next()
            elif self.curr in digits + '-.':
                tokens.append(self.number())
            elif self.curr in ascii_letters:
                tokens.append(self.func_call())
            elif arg and self.curr == ',':
                if len(tokens) == 0 or tokens[-1].type == TT_COMMA:
                    return Error('SyntaxError', 'unexpected ","')
                elif len(tokens) > 1 and tokens[-2].type != TT_COMMA:
                    return Error('SyntaxError', 'expected ","')

                tokens.append(Token(TT_COMMA))
                self.next()
            else:
                return Error('InvalidCharError', repr(self.curr))

            if len(tokens) > 0 and not isinstance(tokens[-1], Token):
                return tokens[-1]

        if arg and len(tokens) > 0 and tokens[-1].type == TT_COMMA:
            return Error('SyntaxError', 'unexpected ","')
        elif arg and len(tokens) > 1 and tokens[-2].type != TT_COMMA:
            return Error('SyntaxError', 'expected ","')

        return tokens

    def string(self):
        quote = self.curr
        string = ''

        self.next()

        while self.curr != quote:
            if not self.curr:
                return Error('SyntaxError', 'unexpected EOF')

            if self.curr == '\\' and (len(string) == 0 or string[-1] != '\\'):
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
        brackets = 1
        in_str = False
        quote = None

        self.next()

        if self.curr == '>': brackets -= 1

        while brackets > 0:
            if not self.curr:
                return Error('SyntaxError', 'unexpected EOF')

            if self.curr == quote and self.code[self.i-1] != '\\':
                in_str = not in_str
                quote = self.curr if not quote and self.curr in '"\'' else None

            if self.curr == '<' and not in_str: brackets += 1

            array_str += self.curr
            self.next()

            if self.curr == '>' and not in_str: brackets -= 1

        self.next()

        array = Lexer(array_str).tokenize(True)

        if isinstance(array, Error): return array

        return Token(TT_ARRAY, array)

    def args(self):
        args = ''
        brackets = 1
        in_str = False
        quote = None

        if self.curr == ')': brackets -= 1

        while brackets > 0:
            if not self.curr:
                return Error('SyntaxError', 'unexpected EOF')

            if self.curr == quote and self.code[self.i-1] != '\\':
                in_str = not in_str
                quote = self.curr if not quote and self.curr in '"\'' else None

            if self.curr == '(' and not in_str: brackets += 1

            args += self.curr
            self.next()

            if self.curr == ')' and not in_str: brackets -= 1

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