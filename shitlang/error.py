class SLError:
    def __init__(self, type_, fn, details=None):
        self.type = type_
        self.fn = fn
        self.details = details

    def __repr__(self) -> str:
        return f'File "{self.fn}":\nError:\n  {self.type}: {self.details}'


class SLSyntaxError(SLError):
    def __init__(self, fn, details=None):
        super().__init__("SyntaxError", fn, details)


class SLTypeError(SLError):
    def __init__(self, fn, details=None):
        super().__init__("TypeError", fn, details)


class SLValueError(SLError):
    def __init__(self, fn, details=None):
        super().__init__("ValueError", fn, details)


class SLBuiltinError(SLError):
    def __init__(self, fn, details=None):
        super().__init__("BuiltinError", fn, details)


class SLRecursionError(SLError):
    def __init__(self, fn, details=None):
        super().__init__("RecursionError", fn, details)


class SLVarNotDefinedError(SLError):
    def __init__(self, fn, details=None):
        super().__init__("VarNotDefinedError", fn, details)


class SLFileNotFoundError(SLError):
    def __init__(self, fn, details=None):
        super().__init__("FileNotFoundError", fn, details)


class SLInvalidCharError(SLError):
    def __init__(self, fn, details=None):
        super().__init__("InvalidCharError", fn, details)


def is_SLerr(obj):
    return isinstance(obj, SLError)
