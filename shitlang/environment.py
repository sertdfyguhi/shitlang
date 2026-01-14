from .context import Context


class Environment:
    def __init__(self, context: Context):
        self.context = context
        self.functions = {}

    def add_func(self, name: str, func: list):
        self.functions[name] = func

    def get_func(self, name: str):
        return self.functions.get(name)

    def has_func(self, name: str):
        return name in self.functions
