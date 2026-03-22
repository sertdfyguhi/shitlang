from ..error import SLValueError


class DictBuiltins:
    def dict_(self, keys: list[str], values: list):
        if len(keys) != len(values):
            raise SLValueError(
                self.context, "arguments 'keys' and 'values' must have the same length"
            )

        return {} if len(keys) == 0 else dict(zip(keys, values))

    def dict_get(self, dict_: dict, key: str):
        return dict_.get(key)

    def dict_set(self, dict_: dict, key: str, value):
        if key == "":
            raise SLValueError(self.context, "argument 'key' cannot be empty")

        dict_ = dict_.copy()
        dict_[key] = value
        return dict_

    def dict_keys(self, dict_: dict):
        return list(dict_.keys())

    def dict_values(self, dict_: dict):
        return list(dict_.values())
