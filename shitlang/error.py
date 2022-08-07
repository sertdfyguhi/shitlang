class Error:
    def __init__(self, type_, details=None):
        self.type = type_
        self.details = details

    def __repr__(self) -> str:
        return f'Error:\n  {self.type}: {self.details}'

class SyntaxError_(Error):
    def __init__(self, details=None):
        super().__init__('SyntaxError', details)

class TypeError_(Error):
    def __init__(self, details=None):
        super().__init__('TypeError', details)

class ValueError_(Error):
    def __init__(self, details=None):
        super().__init__('ValueError', details)

class BuiltinError_(Error):
    def __init__(self, details=None):
        super().__init__('BuiltinError', details)

class RecursionError_(Error):
    def __init__(self, details=None):
        super().__init__('RecursionError', details)

class VarNotDefinedError_(Error):
    def __init__(self, details=None):
        super().__init__('VarNotDefinedError', details)

class FileNotFoundError_(Error):
    def __init__(self, details=None):
        super().__init__('FileNotFoundError', details)

class InvalidCharError_(Error):
    def __init__(self, details=None):
        super().__init__('InvalidCharError', details)
