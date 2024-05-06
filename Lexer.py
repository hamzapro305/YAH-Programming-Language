# Import the necessary constants from the 'globals' module
from globals import KEYWORDS, OPERATORS, PUNCTUATION, TOKEN_TYPES

# Define the Lexer class to tokenize a given source code into a list of tokens
class Lexer:
    # Initialize the Lexer with the source code and set up initial states
    def __init__(self, source_code):
        self.source_code = source_code  # The source code to be tokenized
        self.tokens = []  # A list to hold the generated tokens
        self.current_pos = 0  # Position of the current character in the source code
        self.current_char = source_code[0] if source_code else None  # Current character being processed

    # Method to advance to the next character in the source code
    def advance(self):
        self.current_pos += 1  # Move to the next position
        self.current_char = (
            self.source_code[self.current_pos]
            if self.current_pos < len(self.source_code)  # Check for bounds
            else None  # If out of bounds, set current_char to None
        )

    # Main method to tokenize the source code into tokens
    def tokenize(self):
        # Loop through all characters in the source code
        while self.current_char is not None:
            if self.current_char.isspace():  # If the current character is a space
                self.advance()  # Skip whitespace
            elif self.current_char.isdigit():  # If it's a digit
                self.tokens.append(self.read_number())  # Read the number token
            elif self.current_char.isalpha() or self.current_char == "_":  # If it's an identifier
                self.tokens.append(self.read_identifier())  # Read the identifier or keyword
            elif self.current_char == '"':  # If it's a double quote
                self.tokens.append(self.read_string())  # Read the string literal
            elif self.current_char in OPERATORS:  # If it's an operator
                self.tokens.append(self.read_operator())  # Read the operator token
            elif self.current_char in PUNCTUATION:  # If it's punctuation
                self.tokens.append(self.read_punctuation())  # Read the punctuation token
            else:
                # If it's an unknown character, create an 'unknown' token
                self.tokens.append(
                    {'type': TOKEN_TYPES['UNKNOWN'], 'value': self.current_char}
                )
                self.advance()  # Move to the next character
        
        # Return the list of tokens once the source code has been fully tokenized
        return self.tokens

    # Method to read a number from the source code
    def read_number(self):
        start_pos = self.current_pos  # Remember where the number starts
        while self.current_char is not None and self.current_char.isdigit():  # While it's a digit
            self.advance()  # Keep moving through the number
        # Return a token with the number value
        return {
            'type': TOKEN_TYPES['NUMBER'],  # Define the token type as a number
            'value': self.source_code[start_pos:self.current_pos]  # Extract the number's value
        }
    
    # Method to read an identifier or keyword from the source code
    def read_identifier(self):
        start_pos = self.current_pos  # Remember where the identifier starts
        while (
            self.current_char is not None
            and (self.current_char.isalnum() or self.current_char == "_")  # Valid identifier characters
        ):
            self.advance()  # Keep moving through the identifier
        identifier = self.source_code[start_pos:self.current_pos]  # Extract the identifier
        token_type = (
            TOKEN_TYPES['KEYWORD'] if identifier in KEYWORDS  # Determine if it's a keyword
            else TOKEN_TYPES['IDENTIFIER']  # Otherwise, it's just an identifier
        )
        # Return a token with the identifier's type and value
        return {'type': token_type, 'value': identifier}

    # Method to read a string literal enclosed in double quotes
    def read_string(self):
        self.advance()  # Skip the opening double quote
        start_pos = self.current_pos  # Remember where the string starts
        while self.current_char is not None and self.current_char != '"':  # Loop until the closing quote
            self.advance()  # Move through the string content
        self.advance()  # Skip the closing double quote
        # Return a token with the string's content (excluding the quotes)
        return {
            'type': TOKEN_TYPES['STRING'],  # Define the token type as a string
            'value': self.source_code[start_pos:self.current_pos - 1]  # Extract the string content
        }

    # Method to read an operator from the source code
    def read_operator(self):
        # Check for the special case of '==' operator
        if self.current_char == '=' and (
            self.current_pos + 1 < len(self.source_code)  # Ensure within bounds
            and self.source_code[self.current_pos + 1] == '='  # Next character is also '='
        ):
            self.advance()  # Advance past the first '='
        operator = self.current_char  # Capture the current character (operator)
        self.advance()  # Move to the next character
        # Return a token with the operator's value
        return {
            'type': TOKEN_TYPES['OPERATOR'],  # Define the token type as an operator
            'value': operator  # Store the operator's value
        }

    # Method to read punctuation (like brackets or semicolons)
    def read_punctuation(self):
        punctuation = self.current_char  # Capture the current punctuation character
        self.advance()  # Move to the next character
        # Return a token with the punctuation's value
        return {
            'type': TOKEN_TYPES['PUNCTUATION'],  # Define the token type as punctuation
            'value': punctuation  # Store the punctuation's value
        }
