import os


def shitlang_print(values, array=False):
    # values can come in as tuple
    data = values.copy() if type(values) == list else list(values)

    for i in range(len(data)):
        if type(data[i]) == list:
            data[i] = f"<{shitlang_print(data[i], array=True)}>"
        elif type(data[i]) == bool:
            data[i] = "true" if data[i] else "false"
        elif data[i] == None:
            data[i] = "none"
        elif array and type(data[i]) == str:
            data[i] = repr(data[i])
        else:
            data[i] = str(data[i])

    return (", " if array else " ").join(data)


class IOBuiltins:
    def print(self, *data):
        print(shitlang_print(data))

    def bprint(self, *data):
        print(shitlang_print(data), end="")

    def input(self, prompt: str):
        return input(prompt)

    def file_exists(self, path: str):
        return os.path.isfile(path)

    def read_file(self, path: str):
        with open(path, "r") as f:
            return f.read()

    def write_file(self, path: str, content: str):
        with open(path, "w") as f:
            f.write(content)

    def append_file(self, path: str, content: str):
        with open(path, "a") as f:
            f.write(content)
