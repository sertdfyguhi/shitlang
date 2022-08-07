class Error:
    def __init__(self, type_, fn, details=None):
        self.type = type_
        self.fn = fn
        self.details = details

    def __repr__(self) -> str:
        return f'File "{self.fn}":\nError:\n  {self.type}: {self.details}'

class SyntaxError_(Error):
    def __init__(self, fn, details=None):
        super().__init__('SyntaxError', fn, details)

class TypeError_(Error):
    def __init__(self, fn, details=None):
        super().__init__('TypeError', fn, details)

class ValueError_(Error):
    def __init__(self, fn, details=None):
        super().__init__('ValueError', fn, details)

class BuiltinError_(Error):
    def __init__(self, fn, details=None):
        super().__init__('BuiltinError', fn, details)

class RecursionError_(Error):
    def __init__(self, fn, details=None):
        super().__init__('RecursionError', fn, details)

class VarNotDefinedError_(Error):
    def __init__(self, fn, details=None):
        super().__init__('VarNotDefinedError', fn, details)

class FileNotFoundError_(Error):
    def __init__(self, fn, details=None):
        super().__init__('FileNotFoundError', fn, details)

class InvalidCharError_(Error):
    def __init__(self, fn, details=None):
        super().__init__('InvalidCharError', fn, details)
