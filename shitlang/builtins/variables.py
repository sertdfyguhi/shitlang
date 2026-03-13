class VariableBuiltins:
    def set(self, name: str, value):
        # print("set:", name, value)
        return self.vars.set(name, value)

    def get(self, name: str):
        return self.vars.get(name)

    def delete(self, name: str):
        return self.vars.delete(name)
