from string import whitespace, ascii_letters, digits
from Core import Core

# Create Keywords and Symbols
KEYWORDS = {
    'and': Core.AND, 'begin': Core.BEGIN, 'case': Core.CASE, 'do': Core.DO, 'else': Core.ELSE, 'end': Core.END,
    'for': Core.FOR, 'if': Core.IF, 'in': Core.IN, 'integer': Core.INTEGER, 'is': Core.IS, 'new': Core.NEW, 
    'not': Core.NOT, 'object': Core.OBJECT, 'or': Core.OR, 'print': Core.PRINT, 'procedure': Core.PROCEDURE,
    'read': Core.READ, 'return': Core.RETURN, 'then': Core.THEN
}
SYMBOLS = {
    '+': Core.ADD, '-': Core.SUBTRACT, '*': Core.MULTIPLY, '/': Core.DIVIDE, '<': Core.LESS, ':': Core.COLON,
    ';': Core.SEMICOLON, '.': Core.PERIOD, ',': Core.COMMA, '(': Core.LPAREN, ')': Core.RPAREN, '[': Core.LSQUARE, 
    ']': Core.RSQUARE, '{': Core.LCURL, '}': Core.RCURL
}

class Scanner:

    def __init__(self, text_stream):
        try: 
            self.file = open(text_stream, 'r')
        except FileNotFoundError:
            raise Exception(f"Error: File '{text_stream}' not found.")
        
        # Choosing to do option 2: Read only the first token, and read the next on demand
        self.current_char = self.file.read(1)
        self.current_token = None
        self.token_value = None
        self.nextToken()
        
    def nextToken(self): # Read the next token from the input stream and update accordingly
        self._skipWhitespace() # Skip any leading whitespace characters

        if not self.current_char:
            self.current_token = Core.EOS
            return
        
        if self.current_char.isalpha(): # Either Identifier or Keyword
            self._scanIdOrKeyword()
        elif self.current_char.isdigit(): # Constant
            self._scanConst()
        elif self.current_char == "'": # String literal
            self._scanString()
        elif self.current_char == '=': # Could be either ASSIGN or EQUAL
            self._scanEquals()
        elif self.current_char in SYMBOLS: # Symbol
            self.current_token = SYMBOLS[self.current_char]
            self.token_value = None
            self.current_char = self.file.read(1) # consume symbol
        else:
            print(f"Error: Unexpected character '{self.current_char}' encountered.")
            self.current_token = Core.ERROR
            self.token_value = None  

    def currentToken(self):
        return self.current_token

    def getID(self):
        return self.token_value

    def getString(self):
        return self.token_value

    def getCONST(self):
        return self.token_value
    

    # Defining private helpers
    def _skipWhitespace(self): # Skip/ignore any leading whitespace characters
        while self.current_char and self.current_char in ' \t\n\r':
            self.current_char = self.file.read(1)

    def _scanIdOrKeyword(self): # Scan an identifier or keyword, and update accordingly
        word = ''
        while self.current_char and (self.current_char.isalpha() or self.current_char.isdigit()): 
            word += self.current_char
            self.current_char = self.file.read(1)
        if word in KEYWORDS:
            self.current_token = KEYWORDS[word]
            self.token_value = None
        else:
            self.current_token = Core.ID
            self.token_value = word
    
    def _scanConst(self): # Scan a constant, update accordingly (Make sure it doesn't exceed 8191)
        num_str = ''
        while self.current_char and self.current_char.isdigit():
            num_str += self.current_char
            self.current_char = self.file.read(1)
        value = int(num_str)
        if value > 8191:
            print(f"Error: Constant value {value} exceeds maximum allowed (8191).")
            self.current_token = Core.ERROR
            self.token_value = None
        else:
            self.current_token = Core.CONST
            self.token_value = value

    def _scanString(self): # Scan a string literal, update accordingly (Make sure it is properly terminated)
        result = ''
        self.current_char = self.file.read(1) # consume opening quote
        while self.current_char and self.current_char != "'":
            result += self.current_char
            self.current_char = self.file.read(1)
        if not self.current_char:
            print("ERROR: String literal not terminated.")
            self.current_token = Core.ERROR
            self.token_value = None
        else:
            self.current_char = self.file.read(1) # consume closing quote
            self.current_token = Core.STRING
            self.token_value = result
    
    def _scanEquals(self): # Scan either ASSIGN or EQUAL, update accordingly
        self.current_char = self.file.read(1) # consume '='
        if self.current_char == '=':
            self.current_token = Core.EQUAL
            self.current_char = self.file.read(1) # consume second '='
        else:
            self.current_token = Core.ASSIGN
        self.token_value = None