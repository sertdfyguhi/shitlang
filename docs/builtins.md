# Builtins

## IO Builtins

- `print(*data: any)`: print to console
- `bprint(*data: any)`: print to console with no newline
- `input(prompt: str) -> string`: returns input from console
- `file_exists(path: str) -> bool`: checks if `path` is a file
- `read_file(path: str) -> string`: returns content in `path`
- `write_file(path: str, content: str)`: writes to `path`
- `append_file(path: str, content: str)`: appends to `path`

## Time Builtins

- `sleep(seconds: int | float)`: sleeps for `seconds`
- `now() -> float`: returns unix time now

## Function Builtins

- `function(file: str, params: array = [], allow_use_vars: bool = false) -> function`: creates a function
- `run(func: function, args: array = []) -> any`: runs a function
- `import(file: str, namespace: str = "")`: imports all variables and functions from `file` to `namespace.name`
- `return(value: any = none)`: used in functions to return values and stop execution
- `run_builtin(name: str, args: array) -> any`: builtin to run a builtin and returns the result
- `while(condition: function, loop: function)`: creates a while loop
- `if(condition: function, func: function, else: function = none) -> any`: runs `func` if `condition` is true else run `else_` if there is one
- `try(func: function, catch_func: function)`: if `func` retuens an error, runs `catch_func` with error string passed in

## Variable Builtins

- `set(name: str, value: any)`: set a variable with `value`
- `get(name: str) -> any`: returns the value of a variable
- `delete(name: str)`: delete a variable

## Operator Builtins

- `not(a: bool) -> bool`: returns the opposite of `a`
- `and(a: bool, b: bool) -> bool`: returns true if both `a` and `b` is true if not returns false
- `or(a: any, b: any) -> bool`: returns true or false based on the `or` operator
- `equals(a: any, b: any) -> bool`: returns true if `a` equals `b` if not returns false
- `greater(a: int | float, b: int | float) -> bool`: returns true if `a` is greater than `b`
- `ge(a: int | float, b: int | float) -> bool`: returns true if `a` is greater than or equal `b`
- `less(a: int | float, b: int | float) -> bool`: returns true if `a` is less than `b`
- `le(a: int | float, b: int | float) -> bool`: returns true if `a` is less than or equal `b`
- `add(a: any, b: any, *c: any) -> any`: returns all arguments added together
- `sub(a: int | float, b: int | float, *c: int | float) -> int | float`: returns all arguments subtracted together
- `mul(a: int | float, b: int | float, *c: int | float) -> int | float`: returns all arguments multiplied together
- `div(a: int | float, b: int | float, *c: int | float) -> int | float`: returns all arguments divided together
- `mod(a: int | float, b: int | float) -> int | float`: returns the modulo of `a` and `b`
- `pow(a: int | float, b: int | float) -> int | float`: returns `a` to the power of `b`

## Dictionary Builtins

- `dict(keys: array[str] = [], values: array = []) -> dict`: makes a dictionary from two seperate arrays of keys and value
- `dict(items: array[array[str, any]]) -> dict`: makes a dictionary from an array of items
- `dict_get(dict: dict, key: str) -> any`: returns value of `key` in `dict`
- `dict_set(dict: dict, key: str, value: any, in_place: bool = True) -> dict`: returns `dict` with `key` set as `value`
- `dict_keys(dict: dict) -> array` returns an array of keys in `dict`
- `dict_values(dict: dict) -> array` returns an array of values in `dict`

## String Builtins

- `replace(replace: str, replacement: str, string: str) -> string`: replaces every instance of `replace` with `replacement` in `string` and returns it
- `split(pattern: str, string: str) -> array` splits `string` on every instance of `deliminator` and returns it
- `concat(*strings: str) -> string`: returns all string in strings concatenated
- `format(string: str, *args: any) -> string`: returns formatted `string` using `args`
- `repeat(value: str | array, amount: int) -> string | array`: repeats `value` by `amount`
- `chr(index: int) -> string`: returns the ascii character of ascii code `index`
- `ord(char: str) -> int`: returns the ascii code of ascii character
- `encode_base64(string: str) -> str`: encodes `string` in base64
- `decode_base64(string: str) -> str`: decodes `string` from base4

## Array Builtins

- `get_index(array: array, index: int) -> any`: returns the value of `index` in `array`
- `set_index(array: array, index: int, value: any) -> array`: sets `index` of `array` to `value` and returns it
- `join(array: array[string], separator: str) -> string`: joins `array` using `separator` and returns it
- `remove(array: array, index: int) -> array`: removes `index` from `array` and returns it
- `append(array: array, value: any, index: int = none) -> array`: inserts `value` into `index` of `array` and returns it
- `swap(array: array, index1: int, index2: int) -> array`: swaps `index1` with `index2` in `array` and returns it
- `slice(array: array | string, start: int, end: int = none) -> array | string | none`: returns `array` sliced from `start` to `end`
- `reverse(array: array | string) -> array | string`: returns `array` reversed
- `sum(array: array[int | float]) -> int | float`: adds every number in `array` and returns it
- `min(array: array[int | float]) -> int | float`: returns the minimum number in `array`
- `max(array: array[int | float]) -> int | float`: returns the maximum number in `array`
- `length(value: array | string) -> int`: returns the length of `value`
- `find(array: array | string, value: any) -> array`: returns indexes of all occurences of `value` in `array`
- `find_by(array: array, condition: function, index: bool = false) -> array`: returns values or indicies that match condition in `array`
- `iterate(array: array | string, func: function)`: iterates through `array` and executes `func` for every element
- `map(array: array, func: function) -> array`: runs `func` for each value in `array` and returns the array of returned values from `func`
- `expand(array: array, var_names: array[str])`: expands `array` into variables in `var_names`

## Math Builtins

- `sqrt(x: int | float) -> int | float`: returns the square root of `x`
- `sin(x: int | float) -> float`: returns the sine of `x`
- `cos(x: int | float) -> float`: returns the cosine of `x`
- `tan(x: int | float) -> float`: returns the tangent of `x`
- `asin(x: int | float) -> float`: returns the arcsine of `x`
- `acos(x: int | float) -> float`: returns the arccosine of `x`
- `atan(x: int | float) -> float`: returns the arctangent of `x`
- `round(number: float) -> int`: rounds `number`
- `floor(number: float) -> int`: rounds `number` down to largest number that is less than `number`
- `ceil(number: float) -> int`: rounds `number` up to next largest number
- `random(seed: int | float | string = none) -> float`: returns a pseudo-random float from 0 to 1 and uses `seed` if `seed` is provided

## Type Builtins

- `type(value: any) -> str`: returns the type of `value` as a string
- `to_string(value: any) -> string`: returns `value` converted into a string
- `to_int(value: any) -> int`: returns `value` converted into a int
- `to_float(value: any) -> float`: returns `value` converted into a float
- `to_bool(value: any) -> bool`: returns `value` converted into a bool

## HTTP Builtins

- `http_get(url: str) -> str`: gets `url` and returns the response
- `http_post(url: str, data: str, content_type: str = "text/plain") -> str`: posts to `url` and returns the response
