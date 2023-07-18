# Builtins

## IO Builtins

- `print(*data: any)`: print to console
- `input(prompt: str) -> string`: returns input from console

## Function Builtins

- `function(file: str, params: array = [], allow_use_vars: bool = false) -> function`: creates a function
- `run(func: function, args: array = []) -> any`: runs a function
- `return(value: any = none)`: used in functions to return values and stop execution
- `run_builtin(name: str, args: array) -> any`: builtin to run a builtin and returns the result
- `while(condition: function, loop: function)`: creates a while loop
- `if(condition: function, func: function, else_: function = none) -> any`: runs `func` if `condition` is true else run `else_` if there is one

## Variable Builtins

- `set(name: str, value: any)`: set a variable with `value`
- `get(name: str) -> any`: returns the value of a variable
- `delete(name: str)`: delete a variable

## Operator Builtins

- `not(a: bool) -> bool`: returns the opposite of `a`
- `and(a: bool, b: bool) -> bool`: returns true if both `a` and `b` is true if not returns false
- `or(a: any, b: any) -> bool`: returns true or false based on the `or` operator
- `equals(a: any, b: any) -> bool`: returns true if `a` equals `b` if not returns false
- `not_equals(a: any, b: any) -> bool`: returns the opposite of `equals`
- `greater(a: int | float, b: int | float) -> bool`: returns true if `a` is greater than `b`
- `greater_or_equal(a: int | float, b: int | float) -> bool`: returns true if `a` is greater than or equal `b`
- `less(a: int | float, b: int | float) -> bool`: returns true if `a` is less than `b`
- `less_or_equal(a: int | float, b: int | float) -> bool`: returns true if `a` is less than or equal `b`
- `add(a: any, b: any) -> any`: returns `a` added to `b`
- `subtract(a: int | float, b: int | float) -> int | float`: returns `a` subtracted by `b`
- `multiply(a: int | float, b: int | float) -> int | float`: returns `a` multiplied by `b`
- `divide(a: int | float, b: int | float) -> int | float`: returns `a` divided by `b`
- `modulus(a: int | float, b: int | float) -> int | float`: returns the remainder of `a` divided by `b`
- `power(a: int | float, b: int | float) -> int | float`: returns `a` to the power of `b`

## String Builtins

- `replace(replace: str, replacement: str, string: str) -> string`: replaces every instance of `replace` with `replacement` in `string` and returns it
- `split(pattern: str, string: str) -> array` splits `string` on every instance of `deliminator` and returns it
- `concat(*strings: str) -> string`: returns all string in strings concatenated
- `format(string: str, *args: any) -> string`: returns formatted `string` using `args`
- `repeat(data: str | array, factor: int) -> string | array`: repeats `data` by `factor`

## Array Builtins

- `index(array: array, index: int) -> any`: returns the value of `index` in `array`
- `set_index(index: int, value: any, array: array) -> array`: sets `index` of `array` to `value` and returns it
- `join(separator: str, array: array[string]) -> string`: joins `array` using `separator` and returns it
- `remove(array: array, index: int) -> array`: removes `index` from `array` and returns it
- `append(array: array, value: any, index: int = none) -> array`: inserts `value` into `index` of `array` and returns it
- `swap(index1: int, index2: int, array: array) -> array`: swaps `index1` with `index2` in `array` and returns it
- `slice(value: array | string, start: int, end: int = none) -> array | string | none`: slices `value` from `start` to `end` and returns it
- `reverse(a: array | string) -> array | string`: returns `a` reversed
- `sum(array: array[int | float]) -> int | float`: adds every number in `array` and returns it
- `min(array: array[int | float]) -> int | float`: returns the minimum number in `array`
- `max(array: array[int | float]) -> int | float`: returns the maximum number in `array`
- `length(value: array | string) -> int`: returns the length of `value`
-

## Math Builtins

- `sqrt(a: int | float) -> int | float`: returns the square root of `a`
- `sin(x: int | float) -> float`: returns the sine of `x`
- `cos(x: int | float) -> float`: returns the cosine of `x`
- `tan(x: int | float) -> float`: returns the tangent of `x`
- `asin(x: int | float) -> float`: returns the arcsine of `x`
- `acos(x: int | float) -> float`: returns the arccosine of `x`
- `atan(x: int | float) -> float`: returns the arctangent of `x`
- `round(number: float) -> int`: rounds `number`
- `floor(number: float) -> int`: rounds `number` down to largest number that is less than `number`
- `ceil(number: float) -> int`: rounds `number` up to next largest number

## Type Builtins

- `type(value: any) -> str`: returns the type of `value` as a string
- `to_string(value: any) -> string`: returns `value` converted into a string
- `to_int(value: any) -> int`: returns `value` converted into a int
- `to_float(value: any) -> float`: returns `value` converted into a float
- `to_bool(value: any) -> bool`: returns `value` converted into a bool

## Miscellaneous Builtins

- `chr(a: int) -> string`: returns the ascii character of ascii code(`a`)
- `ord(a: str) -> int`: returns the ascii code of ascii character
- `random(seed: int | float | string = none) -> float`: returns a pseudo-random float from 0 to 1 and uses `seed` if `seed` is provided
- `encode_base64(string: str) -> str`: encodes `string` in base64
- `decode_base64(string: str) -> str`: decodes `string` from base4
