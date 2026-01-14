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

```
~ 0 ~
print(0)
~~

~ 0 condition ~
return(equals(get('input'), '0'))
~~

~ 1 ~
while(function('1 loop condition'), function('1 loop'))
~~

~ 1 condition ~
return(equals(get('input'), '1'))
~~

~ 1 loop condition ~
return(true)
~~

~ 1 loop ~
print(1)
~~

set('input', input(''))
if(function('0 condition'), function('0'))
if(function('1 condition'), function('1'))
```
