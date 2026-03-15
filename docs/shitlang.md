# Learning shitlang

## Printing

```
print("Hello world!")
```

## Variables

```
set("name", "value")
```

## Comments

```
; This is a comment
print('comment')
= This is a
multi line comment = print('multi line comment')
```

## Types

```
1               ; integer
1.2             ; float
true / false    ; boolean
none            ; none
"string"        ; string
<1, 2, 3>       ; array
```

## Pipes

```
; would be equal to print(add(mul(2, 2), 5))
print([2 > mul(_, 2) > add(_, 5)])

; would be equal to encode_base64(repeat(ord(64), 6))
[ord(64) > repeat(_, 6) > encode_base64()]
```

## Lambdas

```
; [> code]number of args
; args are accessed using underscores, so _ would be the first and __ would be the second
run([> print(_, __)]2, <1, 2>)
```

## Functions (File syntax)

### main.shit

```
run(function("function.shit", <"param1", "param2">), <"argument1", "argument2">)
```

### function.shit

```
print(get("param1"), get("param2"))
```

## Functions (Inline syntax)

```
~ function ~
print(get("param1"), get("param2"))
~~

run(function("function", <"param1", "param2">), <"argument1", "argument2">)
```

## If

```
~ condition ~
return(equals(add(1, 2), 3))
~~

~ if ~
print("result of 1 + 2 is 3")
~~

~ else ~
print("result of 1 + 2 is not 3")
~~

if(function("condition"), function("if"), function("else"))
```

## While loop

```
~ condition ~
return(less(get("i"), 1000))
~~

~ loop ~
print(get("i"))
set("i", add(get("i"), 1))
~~

set("i", 0)
while(function("condition"), function("loop.shit"))
```
