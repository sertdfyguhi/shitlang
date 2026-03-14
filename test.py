from shitlang import Lexer, Context, Interpreter, Variables, Environment
from functools import partial
import timeit

code = "print([random() > add(_, 1) > add(_, 20)])"

context = Context("test", is_name=True)
environment = Environment(context)
vars_ = Variables(context)


tokens = Lexer(code, context).tokenize()
# print(tokens)
interpreter = Interpreter(context)
print(interpreter.interpret(tokens))

# print(timeit.timeit(partial(interpreter.interpret, tokens)), "seconds")
