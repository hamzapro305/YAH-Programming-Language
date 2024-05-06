from Lexer import Lexer
from Parser import Parser as parser, SyntaxError

file = open("./program.YAH")
text = file.read()
print("===============================================")
print(text)
print("===============================================")
lexer = Lexer(text)
tokens = lexer.tokenize()

# Parse the tokens to check syntax validity
p = parser(tokens)
try:
    p.parse()  # This will raise SyntaxError if the syntax is invalid
    print("Syntax is valid")
except SyntaxError as e:
    print(f"Syntax Error: {e}")
