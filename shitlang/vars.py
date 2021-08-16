class Variables:
    def __init__(self) -> None:
        self.vars = {}

    def set(self, key, value):
        self.vars[key] = value

    def get(self, key):
        return self.vars[key]