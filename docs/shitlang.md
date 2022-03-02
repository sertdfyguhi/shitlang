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
- This is a
multi line comment -print('multi line comment')
```

## Types
```
1         - integer
1.2       - float
true      - boolean
none      - none
"string"  - string
<1, 2, 3> - array
```

## Functions
### main.shit
```
run(function("function.shit", <"param1", "param2">), <"argument1", "argument2">)
```

### function.shit
```
print(get("param1"), get("param2"))
```

## If
### main.shit
```
if(function("condition.shit"), function("if.shit"), function("else.shit"))
```

### condition.shit
```
return(equals(add(1, 2), 3))
```

### if.shit
```
print("result of 1 + 2 is 3")
```

### else.shit
```
print("result of 1 + 2 is not 3")
```

## While loop
### main.shit
```
set("i", 0)
while(function("condition.shit"), function("loop.shit"))
```

### condition.shit
```
return(less(get("i"), 1000))
```

### loop.shit
```
print(get("i"))
set("i", add(get("i"), 1))
```