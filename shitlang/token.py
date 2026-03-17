TT_FUNC_DEF = "function definition"
TT_FUNC_DEF_END = "function definition end"
TT_LAMBDA_DEF = "lambda definition"

TT_FUNC_CALL = "function call"

TT_UNDERSCORE = "underscore"

TT_STRING = "string"
TT_NUMBER = "number"
TT_ARRAY = "array"
TT_BOOL = "boolean"
TT_NONE = "none"


class Token:
    def __init__(self, type_, start_pos, end_pos, value=None):
        self.type = type_
        self.value = value

        self.start_pos = start_pos
        self.end_pos = end_pos

    def __repr__(self):
        return f"{self.type}: {repr(self.value)}"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Token):
            return self.value == o

        return self.type == o.type and self.value == o.value
