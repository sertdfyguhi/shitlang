# shitlang

![Certified: Shit](https://img.shields.io/badge/Certified-Shit-success)

please dont use this it's named shitlang for a reason  
[docs here](https://github.com/sertdfyguhi/shitlang/blob/master/docs/shitlang.md)

## install

1. download source code by cloning repository or downloading the source zip from github

```sh
git clone https://github.com/sertdfyguhi/shitlang
```

2. run shitlang.py using python3

```sh
python3 shitlang.py
```

## todo

- [x] escape characters
- [x] somehow implement if, ~~else if~~ and else
- [x] arrays
- [x] array builtins
- [x] documentation
- [x] new lexer
  - [x] string
  - [x] numbers
  - [x] arrays
  - [x] func calls
  - [x] comments
- [ ] rewrite shitlang.py

## examples

### hello world

```
print("Hello World!")
```

### quine

```
set('x', "set('x', {})print(format(get('x'), add(chr(34), add(get('x'), chr(34)))))")print(format(get('x'), add(chr(34), add(get('x'), chr(34)))))
```

### truth machine

#### main.shit

```
set('input', input(''))
if(function('0condition.shit'), function('0.shit'))
if(function('1condition.shit'), function('1.shit'))
```

#### 0condition.shit

```
return(equals(get('input'), '0'))
```

#### 1condition.shit

```
return(equals(get('input'), '1'))
```

#### 0.shit

```
print(0)
```

#### 1.shit

```
while(function('1loop_condition.shit'), function('1loop.shit'))
```

#### 1loop_condition.shit

```
return(True)
```

#### 1loop.shit

```
print(1)
```
