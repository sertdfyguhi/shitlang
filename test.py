from shitlang import Lexer, Context, Interpreter, Variables, Environment
from functools import partial
import timeit

code = "~ name ~ set() ~ sex ~ add() ~ a~"

context = Context("test", is_name=True)
environment = Environment(context)
vars_ = Variables(context)


tokens = Lexer(code, context).tokenize()
interpreter = Interpreter(context)

print(timeit.timeit(partial(interpreter.interpret, tokens)), "seconds")
