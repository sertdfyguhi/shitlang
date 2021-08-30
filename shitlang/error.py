class Error:
    def __init__(self, type_, details=None):
        self.type = type_
        self.details = details

    def __repr__(self) -> str:
        return f'Error:\n  {self.type}: {self.details}'