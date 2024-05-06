from Lexer import Lexer
from Parser import Parser as parser, SyntaxError
import sys

if(len(sys.argv) > 1):
    file = open(sys.argv[1])
    text = file.read()
    print("===============================================")
    print(text)
    print("===============================================")
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    for i, token in enumerate(tokens):
        pass
        # print(f"{token['type']} {token['value']}")

    # Parse the tokens to check syntax validity
    p = parser(tokens)
    try:
        p.parse()  # This will raise SyntaxError if the syntax is invalid
        print("Syntax is valid")
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
else:
    raise SystemError("No Program File Found")
