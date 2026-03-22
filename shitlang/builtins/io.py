import os


def print_value(value, true_string: bool = True):
    match value:
        case list():
            return (
                f"<{" ,".join([print_value(el, true_string=False) for el in value])}>"
            )

        case bool():
            return "true" if value else "false"

        case dict():
            out = ", ".join(
                [
                    f"{key}: {print_value(value[key], true_string=False)}"
                    for key in value
                ]
            )
            return f"dict({out})"

        case str():
            return value if true_string else repr(value)

        case None:
            return "none"

        case _:
            return str(value)


class IOBuiltins:
    def print(self, *data):
        print(" ".join([print_value(value) for value in data]))

    def bprint(self, *data):
        print(" ".join([print_value(value) for value in data]), end="")

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
