from Lexer import Lexer
from Parser import Parser as parser, SyntaxError
import sys

if(len(sys.argv) > 1):
    file = open(sys.argv[1])
    text = file.read()
    print(text)
    lexer = Lexer(text)
    tokens = lexer.tokenize()

else:
    raise SystemError("No Program File Found")
