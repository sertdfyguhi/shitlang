from colorama import Fore, Style

_BOLD = "\033[1m"


class SLError:
    def __init__(self, type_, context, details=None):
        self.type = type_
        self.context = context
        self.details = details

    def __repr__(self) -> str:
        return f'{Fore.RED}{_BOLD}File "{self.context.fn}":{Style.RESET_ALL}{Fore.RED}\nError:\n  {self.type}: {self.details}{Style.RESET_ALL}'


class SLSyntaxError(SLError):
    def __init__(self, context, details=None):
        super().__init__("SyntaxError", context, details)


class SLTypeError(SLError):
    def __init__(self, context, details=None):
        super().__init__("TypeError", context, details)


class SLValueError(SLError):
    def __init__(self, context, details=None):
        super().__init__("ValueError", context, details)


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


def is_SLerr(obj):
    return isinstance(obj, SLError)
