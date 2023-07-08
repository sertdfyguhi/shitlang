from .utils import create_typeerror


class VariableBuiltins:
    def set(self, name, value):
        if type(name) != str:
            return create_typeerror(self.fn, "name", "string")

        return self.vars.set(name, value)

    def get(self, name):
        if type(name) != str:
            return create_typeerror(self.fn, "name", "string")
        return self.vars.get(name)

    def delete(self, name):
        if type(name) != str:
            return create_typeerror(self.fn, "name", "string")
        return self.vars.delete(name)
