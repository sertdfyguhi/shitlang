from typing import Any

from ..error import SLValueError


class DictBuiltins:
    def dict_(self, keys: list[str] | list[list] = [], values: list = []):
        if len(values) == 0:
            if len(keys) == 0:
                return {}

            # keys can be an array of items, eg [['a', 1], ['b', 2]]
            dictionary = {}

            for item in keys:
                if len(item) != 2:
                    raise SLValueError(
                        self.context,
                        "argument 'items' must be an array of arrays with two values",
                    )
                elif type(item[0]) != str:
                    raise SLValueError(
                        self.context,
                        "argument 'items' must be an array of arrays with a string and a value",
                    )

                dictionary[item[0]] = item[1]

            return dictionary
        else:
            if len(keys) != len(values):
                raise SLValueError(
                    self.context,
                    "arguments 'keys' and 'values' must have the same length",
                )

            return dict(zip(keys, values))

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
