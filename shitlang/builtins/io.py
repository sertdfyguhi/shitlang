from .utils import create_typeerror


class IOBuiltins:
    def print(self, *data):
        print(self._print(data))

    def _print(self, values, array=False):
        data = values if type(values) == list else list(values)

        for i in range(len(data)):
            if type(data[i]) == list:
                data[i] = f"<{self._print(data[i], True)}>"
            elif type(data[i]) == bool:
                data[i] = "true" if data[i] else "false"
            elif data[i] == None:
                data[i] = "none"
            elif array and type(data[i]) == str:
                data[i] = repr(data[i])
            else:
                data[i] = str(data[i])

        return (", " if array else " ").join(data)

    def input(self, prompt):
        if type(prompt) != str:
            return create_typeerror(self.context, "prompt", "string")

        return input(prompt)
