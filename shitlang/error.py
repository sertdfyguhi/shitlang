from colorama import Fore, Style

_BOLD = "\033[1m"


class SLError(Exception):
    def __init__(self, type_, context, details=None):
        self.type = type_
        self.context = context
        self.details = details

        super().__init__(details)

    def __str__(self):
        end_pos_detail = f" to {self.context.end_pos}" if self.context.end_pos else ""
        return f'{Fore.RED}{_BOLD}File "{self.context.fn}" on {self.context.pos}{end_pos_detail}:{Style.RESET_ALL}{Fore.RED}\n{self.type}: {Style.RESET_ALL}{self.details}'


class SLSyntaxError(SLError):
    def __init__(self, context, details=None):
        super().__init__("SyntaxError", context, details)


class SLTypeError(SLError):
    def __init__(self, context, details=None):
        super().__init__("TypeError", context, details)


class SLValueError(SLError):
    def __init__(self, context, details=None):
        super().__init__("ValueError", context, details)


class SLIndexError(SLError):
    def __init__(self, context, details=None):
        super().__init__("IndexError", context, details)


class SLBuiltinError(SLError):
    def __init__(self, context, details=None):
        super().__init__("BuiltinError", context, details)


class SLRecursionError(SLError):
    def __init__(self, context, details=None):
        super().__init__("RecursionError", context, details)


class SLVarNotDefinedError(SLError):
    def __init__(self, context, details=None):
        super().__init__("VarNotDefinedError", context, details)


class SLFileNotFoundError(SLError):
    def __init__(self, context, details=None):
        super().__init__("FileNotFoundError", context, details)


class SLInvalidCharError(SLError):
    def __init__(self, context, details=None):
        super().__init__("InvalidCharError", context, details)
