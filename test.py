from shitlang import Lexer, Context

code = "~ name ~ set() ~ sex ~ add() ~ a~"

print(Lexer(code, Context("test", is_name=True)).tokenize())
