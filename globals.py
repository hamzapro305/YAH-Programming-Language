# Token types
TOKEN_TYPES = {
    'KEYWORD': 'KEYWORD',
    'IDENTIFIER': 'IDENTIFIER',
    'NUMBER': 'NUMBER',
    'STRING': 'STRING',
    'OPERATOR': 'OPERATOR',
    'PUNCTUATION': 'PUNCTUATION',
    'WHITESPACE': 'WHITESPACE',
    'UNKNOWN': 'UNKNOWN'
}

# Keywords and operators specific to your language
KEYWORDS = {'if', 'else', 'while', 'for', 'function', 'return', 'MANLO'}
OPERATORS = {'+', '-', '*', '/', '=', '==', '!=', '>', '<', '>=', '<='}
ARITHEMATIC_OPERATOR = {'+', '-', '*', '/'}
LOGICAL_OPERATOR = {'==', '!=', '>', '<', '>=', '<='}
ASSIGNMENT_OPERATOR = {'='}
PUNCTUATION = {'(', ')', '{', '}', ';', ',', '.'}