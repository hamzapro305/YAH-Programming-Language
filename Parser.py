# Define a custom exception for syntax errors
class SyntaxError(Exception):
    """Custom exception for syntax errors."""
    def __init__(self, message, token=None):
        super().__init__(message)  # Call the base class constructor
        self.token = token  # Optionally, store the token where the error occurred


# Define a Parser class for parsing a list of tokens into a meaningful structure
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Store the list of tokens to be parsed
        self.current_pos = 0  # Initialize the current token position

        # Detect functions in the token list
        self.funcs = self.detect_funcs(tokens)

        # Check if there is a main function
        self.main_validity()

    # Method to ensure there's a main function in the code
    def main_validity(self):
        is_main = False  # Flag to check if 'main' function is found
        # Loop through the detected functions
        for func in self.funcs:
            if func['name'] == 'main':  # If there's a 'main' function
                is_main = True

        if not is_main:  # If 'main' function is not found
            raise SyntaxError("No Main Function detected")  # Raise a syntax error
    
    # Method to detect functions in the list of tokens
    def detect_funcs(self, tokens):
        funcs = []  # List to hold detected functions
        # Loop through the tokens to find function declarations
        for i, token in enumerate(tokens):
            if (
                token['type'] == "KEYWORD"  # If the token is a keyword
                and token['value'] == "function"  # and it's 'function'
            ):
                funcs.append({
                    'loc': i,  # Store the location in the token list
                    'name': tokens[i + 1]['value'],  # Store the function name
                })
        return funcs  # Return the list of detected functions

    # Method to get the current token in the list
    def current_token(self):
        return self.tokens[self.current_pos]

    # Method to advance to the next token in the list
    def advance(self):
        self.current_pos += 1  # Increment the current position

    # Method to move the cursor to a specific location in the token list
    def move_cursor(self, loc):
        self.current_pos = loc  # Set the current position

    # Method to check if the current token matches an expected type and value
    def expect(self, token_type, expected_value=None):
        token = self.current_token()  # Get the current token
        # Check if it matches the expected type and value (if provided)
        if token['type'] == token_type and (
            expected_value is None or token['value'] == expected_value
        ):
            self.advance()  # Advance to the next token
            return token  # Return the current token
        raise SyntaxError(  # Raise an error if the token doesn't match
            f"Expected {token_type} " +
            (f"'{expected_value}'" if expected_value else ""),
            token,
        )

    # Main parsing method to validate the syntax of the code
    def parse(self):
        # Loop through the detected functions
        for fun in self.funcs:
            self.move_cursor(fun['loc'])  # Move to the function's location
            self.parse_function()  # Parse the function declaration

    # Method to parse a function declaration
    def parse_function(self):
        self.expect('KEYWORD', 'function')  # Expect 'function' keyword
        self.expect('IDENTIFIER')  # Expect the function name
        self.expect('PUNCTUATION', '(')  # Expect '(' for parameters

        # Check if there are parameters
        if self.current_token()['type'] == 'IDENTIFIER':
            self.parse_parameters()  # Parse the function parameters

        self.expect('PUNCTUATION', ')')  # Expect closing parenthesis
        self.expect('PUNCTUATION', '{')  # Expect opening curly brace for function body
        self.parse_statements()  # Parse the function body statements
        self.expect('PUNCTUATION', '}')  # Expect closing curly brace

    # Method to parse function parameters (comma-separated identifiers)
    def parse_parameters(self):
        while True:
            self.expect('IDENTIFIER')  # Expect parameter identifier
            current_token = self.current_token()  # Get the current token
            # Check if we're at the closing parenthesis for parameters
            if current_token['type'] == 'PUNCTUATION' and current_token['value'] == ')':
                break  # End of parameters
            elif current_token['type'] == 'PUNCTUATION' and current_token['value'] == ',':
                self.advance()  # Move to the next parameter
            else:
                raise SyntaxError("Unexpected parameter syntax")  # Raise error for invalid parameter

    # Method to parse statements within the function body
    def parse_statements(self):
        # Continue parsing until the closing curly brace of the function body
        while self.current_token()['value'] != '}':
            current_token = self.current_token()  # Get the current token

            if current_token['type'] == 'KEYWORD':  # Handle keyword-based statements
                if current_token['value'] == 'return':
                    self.parse_return_statement()  # Parse 'return' statement
                elif current_token['value'] == 'if':
                    self.parse_if_statement()  # Parse 'if' statement
                elif current_token['value'] == 'while':
                    self.parse_while_statement()  # Parse 'while' statement
                elif current_token['value'] == 'for':
                    self.parse_for_statement()  # Parse 'for' statement
                else:
                    raise SyntaxError(f"Unexpected keyword '{current_token['value']}'")  # Invalid keyword
            elif current_token['type'] == 'IDENTIFIER':  # Handle identifier-based statements
                self.parse_assignment_or_function_call()  # Could be variable assignment or function call
            else:
                raise SyntaxError(f"Unexpected token '{current_token['value']}'")  # Invalid token type

    # Method to parse a return statement
    def parse_return_statement(self):
        self.expect('KEYWORD', 'return')  # Expect 'return' keyword
        self.parse_expression()  # Parse the expression after 'return'
        self.expect('PUNCTUATION', ';')  # Expect semicolon at the end of 'return' statement

    # Method to parse an expression, which could include operations or function calls
    def parse_expression(self):
        if self.current_token()['type'] in {'IDENTIFIER', 'NUMBER'}:
            self.advance()  # Move past the identifier or number
            # Handle operations in expressions
            while (
                self.current_token()['type'] == 'OPERATOR'
                and self.current_token()['value'] in {'+', '-', '*', '/'}
            ):
                self.advance()  # Move past the operator
                # Expect another identifier or number after operator
                if self.current_token()['type'] not in {'IDENTIFIER', 'NUMBER'}:
                    raise SyntaxError("Expected identifier or number after operator")
                self.advance()  # Move past the next identifier or number

        elif self.current_token()['type'] == 'STRING':
            self.advance()  # Handle strings in expressions
        else:
            raise SyntaxError("Unexpected expression syntax")  # Raise error for invalid expression

    # Method to parse a variable assignment or function call
    def parse_assignment_or_function_call(self):
        identifier = self.expect('IDENTIFIER')  # Get the variable/function name

        if self.current_token()['value'] == '(':
            self.parse_function_call()  # If it's a function call
        elif self.current_token()['value'] == '=':
            self.parse_assignment()  # If it's a variable assignment
        else:
            raise SyntaxError("Expected '(' or '=' after identifier")  # Invalid syntax

    # Method to parse a function call with a list of expressions
    def parse_function_call(self):
        self.expect('PUNCTUATION', '(')  # Opening parenthesis
        self.parse_expression_list()  # Parse function call parameters
        self.expect('PUNCTUATION', ')')  # Closing parenthesis
        self.expect('PUNCTUATION', ';')  # Semicolon at the end of function call

    # Method to parse a list of expressions (comma-separated)
    def parse_expression_list(self):
        while True:
            self.parse_expression()  # Parse each expression in the list
            # Check if the list ends with a closing parenthesis
            if (
                self.current_token()['type'] == 'PUNCTUATION' 
                and self.current_token()['value'] == ')'
            ):
                break
            elif (
                self.current_token()['type'] == 'PUNCTUATION' 
                and self.current_token()['value'] == ','
            ):
                self.advance()  # Move to the next expression
            else:
                raise SyntaxError("Unexpected expression list syntax")  # Invalid expression list

    # Method to parse a variable assignment
    def parse_assignment(self):
        self.expect('OPERATOR', '=')  # Expect assignment operator '='
        self.parse_expression()  # Parse the value being assigned
        self.expect('PUNCTUATION', ';')  # Expect semicolon at the end of the assignment

    # Method to parse an 'if' or 'if-else' statement
    def parse_if_statement(self):
        self.expect('KEYWORD', 'if')  # Expect 'if' keyword
        self.expect('PUNCTUATION', '(')  # Opening parenthesis for the condition
        self.parse_expression()  # Parse the 'if' condition
        self.expect('PUNCTUATION', ')')  # Closing parenthesis

        # Parse the 'if' block statements
        self.expect('PUNCTUATION', '{')  # Opening curly brace
        self.parse_statements()  # Parse statements inside the 'if' block
        self.expect('PUNCTUATION', '}')  # Closing curly brace

        # Check if there's an 'else' block
        if (
            self.current_token()['type'] == 'KEYWORD'
            and self.current_token()['value'] == 'else'
        ):
            self.advance()  # Move to 'else'
            self.expect('PUNCTUATION', '{')  # Opening curly brace
            self.parse_statements()  # Parse statements inside the 'else' block
            self.expect('PUNCTUATION', '}')  # Closing curly brace

    # Method to parse a 'while' loop
    def parse_while_statement(self):
        self.expect('KEYWORD', 'while')  # Expect 'while' keyword
        self.expect('PUNCTUATION', '(')  # Opening parenthesis for the condition
        self.parse_expression()  # Parse the loop condition
        self.expect('PUNCTUATION', ')')  # Closing parenthesis

        # Parse the statements within the 'while' block
        self.expect('PUNCTUATION', '{')  # Opening curly brace
        self.parse_statements()  # Parse statements within the 'while' block
        self.expect('PUNCTUATION', '}')  # Closing curly brace

    # Method to parse a simple 'for' loop
    def parse_for_statement(self):
        self.expect('KEYWORD', 'for')  # Expect 'for' keyword
        self.expect('PUNCTUATION', '(')  # Opening parenthesis

        # Parse the initialization expression in the 'for' loop
        self.parse_assignment_or_function_call()  # e.g., variable initialization or assignment

        # Parse the loop condition
        self.parse_expression()

        # Parse the increment/decrement operation in the 'for' loop
        self.parse_expression()

        self.expect('PUNCTUATION', ')')  # Closing parenthesis

        # Parse the statements within the 'for' loop block
        self.expect('PUNCTUATION', '{')  # Opening curly brace
        self.parse_statements()  # Parse statements in the 'for' block
        self.expect('PUNCTUATION', '}')  # Closing curly brace
